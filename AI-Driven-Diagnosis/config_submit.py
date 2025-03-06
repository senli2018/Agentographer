config = {
    "datapath": "E:/data/lung/test_image",
    "preprocess_result_path": "./prep_result/",
    "outputfile": "prediction.csv",
    "detector_model": "net_detector",
    "detector_param": "./model/detector.ckpt",
    "classifier_model": "net_classifier",
    "classifier_param": "./model/classifier.ckpt",
    "n_gpu": 8,
    "n_worker_preprocessing": 1,
    "use_exsiting_preprocessing": False,
    "skip_preprocessing": True,
    "skip_detect": False,
}
