from preprocessing import full_prep
from config_submit import config as config_submit
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pydicom
import time
import torch

from layers import acc

from utils import *
from split_combine import SplitComb
from importlib import import_module
from preprocessing.full_prep import savenpy_single

def det_data_process(prep_result_path, config1):
    imgs = np.load(os.path.join(prep_result_path, 'image_0_clean.npy'))
    nz, nh, nw = imgs.shape[1:]
    margin = int(32)
    sidelen = int(144)
    stride =  int(config1['stride']) 
    pad_value= int(config1['pad_value'])
    split_comber = SplitComb(sidelen,int(config1['max_stride']),stride,margin,pad_value= pad_value)
    pz = int(np.ceil(float(nz) / stride)) * stride
    ph = int(np.ceil(float(nh) / stride)) * stride
    pw = int(np.ceil(float(nw) / stride)) * stride
    imgs = np.pad(imgs, [[0,0],[0, pz - nz], [0, ph - nh], [0, pw - nw]], 'constant',constant_values = pad_value)
    xx,yy,zz = np.meshgrid(np.linspace(-0.5,0.5,int(imgs.shape[1]/stride)),
                            np.linspace(-0.5,0.5,int(imgs.shape[2]/stride)),
                            np.linspace(-0.5,0.5,int(imgs.shape[3]/stride)),indexing ='ij')
    coord = np.concatenate([xx[np.newaxis,...], yy[np.newaxis,...],zz[np.newaxis,:]],0).astype('float32')
    imgs, nzhw = split_comber.split(imgs)
    coord2, nzhw2 = split_comber.split(coord,
                                            side_len = int(split_comber.side_len/stride),
                                            max_stride = int(split_comber.max_stride/stride),
                                            margin = int(split_comber.margin/stride))
    assert np.all(nzhw==nzhw2)
    imgs = (imgs.astype(np.float32)-128)/128
    
    return torch.from_numpy(imgs.astype(np.float32)), torch.from_numpy(coord2.astype(np.float32))

def det_inference(data_path, output_path):
    prep_result_path = config_submit['preprocess_result_path']

    savenpy_single('image_0',prep_folder=output_path,data_path=data_path,use_existing=True)

    nodmodel = import_module(config_submit['detector_model'].split('.py')[0])
    config1, nod_net, loss, get_pbb = nodmodel.get_model()
    checkpoint = torch.load(config_submit['detector_param'])
    nod_net.load_state_dict(checkpoint['state_dict'])
    torch.cuda.set_device(0)
    nod_net = nod_net.cuda()
    nod_net.eval()
    input, inputcoord = det_data_process(prep_result_path, config1)
    output, feature = nod_net(input.cuda(), inputcoord.cuda())
    return output

def cas_inference(data_path):
    casemodel = import_module(config_submit['classifier_model'].split('.py')[0])
    casenet = casemodel.CaseNet(topk=5)
    config2 = casemodel.config
    bboxpath = config2['bboxpath']
    checkpoint = torch.load(config_submit['classifier_param'])
    casenet.load_state_dict(checkpoint['state_dict'])
    x,coord = cas_data_process(data_path, bboxpath)
    nodulePred,casePred, result = casenet(x,coord)
    return nodulePred, casePred, result
def cas_data_process(prep_result_path,bboxpath):
    imgs = np.load(os.path.join(prep_result_path, 'image_0_clean.npy'))
    pbb = np.load(os.path.join(bboxpath,'image_0_pbb.npy'))
    return imgs, pbb

def get_lung_nod(image_path):
    output_path = './prep_result/'
    dcm = pydicom.dcmread(image_path)
    spacing = dcm.PixelSpacing
    box_list, _ = det_inference(image_path, output_path)
    cls_list,_, pro_list = cas_inference(image_path, output_path)

    return box_list, cls_list, pro_list,spacing


app = FastAPI()

@app.post('/lung/intact/')
def lung_node(image: UploadFile=File(None)):
    file = image
    try:
        if file is None:
            image_path = "2.dcm"
        else:
            filename = f"{time.time()}_{file.filename}"
            image_path = os.path.join(os.getcwd(), "origin_images",filename)

        box_list, cls_list, pro_list,spacing = get_lung_nod(image_path)
        result_list = []
        for i in range(len(box_list)):
            box_result = box_list[i]
            cls_result = cls_list[i]
            pro_result = pro_list[i]
            box_size = (box_result[0]-box_result[1])*(box_result[3]-box_result[2])*(box_result[5]-box_result[6])
            nodule_size = box_size* spacing*spacing*spacing
            if nodule_size>3:
                nodule_size_bool = True
            else:
                nodule_size_bool = False

            data = {
                'nodule_size': nodule_size_bool,
                'nodule_cls': cls_result,
                'nodule_pred': float(pro_result),
                'nodule_local': box_result
            }
            result_list.append(data)

        return result_list
    except Exception as e:
        return {'error': str(e)}


if __name__ == "__main__":
    data_path = 'test_image/image_0'
    box_path = './'
    output_path = './prep_result/'
    det_inference(data_path, output_path)