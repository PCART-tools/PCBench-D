def generate_models():
    sc = SomeClass()
    for model in models:
        print('update-caffe2-models.py:  generating', model)
        caffe2_model_dir = sc._caffe2_model_dir(model)
        onnx_model_dir, onnx_models_dir = sc._onnx_model_dir(model)
        subprocess.check_call(['echo', model])
        with open(os.path.join(caffe2_model_dir, 'value_info.json'), 'r') as f:
            value_info = f.read()
        subprocess.check_call([
            'convert-caffe2-to-onnx',
            '--caffe2-net-name', model,
            '--caffe2-init-net', os.path.join(caffe2_model_dir, 'init_net.pb'),
            '--value-info', value_info,
            '-o', os.path.join(onnx_model_dir, 'model.pb'),
            os.path.join(caffe2_model_dir, 'predict_net.pb')
        ])
        subprocess.check_call([
            'tar',
            '-czf',
            model + '.tar.gz',
            model
        ], cwd=onnx_models_dir)
