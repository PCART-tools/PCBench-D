def download_models():
    sc = SomeClass()
    for model in models:
        print('update-caffe2-models.py:  downloading', model)
        caffe2_model_dir = sc._caffe2_model_dir(model)
        onnx_model_dir, onnx_models_dir = sc._onnx_model_dir(model)
        if not os.path.exists(caffe2_model_dir):
            sc._download(model)
        if not os.path.exists(onnx_model_dir):
            sc._prepare_model_data(model)
