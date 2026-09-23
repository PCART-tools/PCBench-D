def cleanup():
    sc = SomeClass()
    for model in models:
        onnx_model_dir, onnx_models_dir = sc._onnx_model_dir(model)
        os.remove(os.path.join(os.path.dirname(onnx_model_dir), model + '.tar.gz'))
