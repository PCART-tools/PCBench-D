def exportTest(self, model, inputs, rtol=1e-2, atol=1e-7, opset_versions=None):
    opset_versions = opset_versions if opset_versions else [7, 8, 9, 10, 11, 12, 13, 14]

    for opset_version in opset_versions:
        self.opset_version = opset_version
        self.onnx_shape_inference = True
        run_model_test(self, model, False,
                       input=inputs, rtol=rtol, atol=atol)

        if self.is_script_test_enabled and opset_version > 11:
            script_model = torch.jit.script(model)
            run_model_test(self, script_model, False,
                           input=inputs, rtol=rtol, atol=atol)
