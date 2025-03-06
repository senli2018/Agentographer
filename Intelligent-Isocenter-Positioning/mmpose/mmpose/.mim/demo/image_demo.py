# Copyright (c) OpenMMLab. All rights reserved.
from argparse import ArgumentParser

from mmcv.image import imread

from mmpose.apis import inference_topdown, init_model
from mmpose.registry import VISUALIZERS
from mmpose.structures import merge_data_samples
import cv2

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('img', help='Image file')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument('--out-file', default=None, help='Path to output file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--draw-heatmap',
        action='store_true',
        help='Visualize the predicted heatmap')
    parser.add_argument(
        '--show-kpt-idx',
        action='store_true',
        default=False,
        help='Whether to show the index of keypoints')
    parser.add_argument(
        '--skeleton-style',
        default='mmpose',
        type=str,
        choices=['mmpose', 'openpose'],
        help='Skeleton style selection')
    parser.add_argument(
        '--kpt-thr',
        type=float,
        default=0.3,
        help='Visualizing keypoint thresholds')
    parser.add_argument(
        '--radius',
        type=int,
        default=3,
        help='Keypoint radius for visualization')
    parser.add_argument(
        '--thickness',
        type=int,
        default=1,
        help='Link thickness for visualization')
    parser.add_argument(
        '--alpha', type=float, default=0.8, help='The transparency of bboxes')
    parser.add_argument(
        '--show',
        action='store_true',
        default=False,
        help='whether to show img')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # build the model from a config file and a checkpoint file
    if args.draw_heatmap:
        cfg_options = dict(model=dict(test_cfg=dict(output_heatmaps=True)))
    else:
        cfg_options = None

    model = init_model(
        args.config,
        args.checkpoint,
        device=args.device,
        cfg_options=cfg_options)

    # init visualizer
    model.cfg.visualizer.radius = args.radius
    model.cfg.visualizer.alpha = args.alpha
    model.cfg.visualizer.line_width = args.thickness

    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.set_dataset_meta(
        model.dataset_meta, skeleton_style=args.skeleton_style)

    # inference a single image
    batch_results = inference_topdown(model, args.img)
    results = merge_data_samples(batch_results)
    # 获取关键点的结果
    keypoints = results.pred_instances['keypoints']
    left_eye_point = keypoints[0, 1] # 左眼
    left_ear_point = keypoints[0, 3] # 左耳
    right_ear_point = keypoints[0, 4] # 右耳
    left_sholder_point = keypoints[0, 5] # 左肩
    right_sholder_point = keypoints[0, 6] # 右肩
    
    # TODO 1. 定义脖子所在像素在裁剪图像前的像素位置
    # TODO 2. 定义左肩所在像素在裁剪图像前的像素位置
    # TODO 3. 定义侧面扫描床标记线到左肩的垂直距离

    # show the results
    img = imread(args.img, channel_order='rgb')
    cv2.circle(img, (int(left_sholder_point[0]), int(left_sholder_point[1])), 5, (255, 0, 0), -1)
    cv2.imwrite("tmp_result.png", img)
    visualizer.add_datasample(
        'result',
        img,
        data_sample=results,
        draw_gt=False,
        draw_bbox=True,
        kpt_thr=args.kpt_thr,
        draw_heatmap=args.draw_heatmap,
        show_kpt_idx=args.show_kpt_idx,
        skeleton_style=args.skeleton_style,
        show=args.show,
        out_file=args.out_file)


if __name__ == '__main__':
    main()
