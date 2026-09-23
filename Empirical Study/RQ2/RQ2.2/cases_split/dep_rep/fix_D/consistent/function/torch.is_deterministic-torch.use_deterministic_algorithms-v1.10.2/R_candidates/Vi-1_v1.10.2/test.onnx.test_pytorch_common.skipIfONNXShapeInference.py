def skipIfONNXShapeInference(onnx_shape_inference):
    def skip_dec(func):
        def wrapper(self):
            if self.onnx_shape_inference is onnx_shape_inference:
                raise unittest.SkipTest("Skip verify test for unsupported opset_version")
            return func(self)
        return wrapper
    return skip_dec
