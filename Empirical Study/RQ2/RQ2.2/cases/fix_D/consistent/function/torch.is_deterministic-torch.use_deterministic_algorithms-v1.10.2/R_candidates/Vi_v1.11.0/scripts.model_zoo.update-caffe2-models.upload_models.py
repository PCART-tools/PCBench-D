def upload_models():
    sc = SomeClass()
    for model in models:
        print('update-caffe2-models.py:  uploading', model)
        onnx_model_dir, onnx_models_dir = sc._onnx_model_dir(model)
        subprocess.check_call([
            'aws',
            's3',
            'cp',
            model + '.tar.gz',
            "s3://download.onnx/models/{}.tar.gz".format(model),
            '--acl', 'public-read'
        ], cwd=onnx_models_dir)
