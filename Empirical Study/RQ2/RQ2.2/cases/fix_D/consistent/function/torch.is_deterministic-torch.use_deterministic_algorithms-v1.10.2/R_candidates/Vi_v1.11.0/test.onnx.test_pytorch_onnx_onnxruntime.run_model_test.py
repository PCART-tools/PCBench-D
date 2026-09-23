def run_model_test(self, model, batch_size=2, state_dict=None,
                   input=None, use_gpu=True, rtol=0.001, atol=1e-7,
                   do_constant_folding=True, dynamic_axes=None,
                   test_with_inputs=None, input_names=None,
                   output_names=None, fixed_batch_size=False,
                   dict_check=True, training=None,
                   remained_onnx_input_idx=None, flatten=True):
    if training is not None and training == torch.onnx.TrainingMode.TRAINING:
        model.train()
    elif training is None or training == torch.onnx.TrainingMode.EVAL:
        model.eval()
    if input is None:
        input = torch.randn(batch_size, 3, 224, 224, requires_grad=True)
    with torch.no_grad():
        if isinstance(input, torch.Tensor):
            input = (input,)
        # In-place operators will update input tensor data as well.
        # Thus inputs are replicated before every forward call.
        if isinstance(input, dict):
            input = (input,)
        input_args = copy.deepcopy(input)
        input_kwargs = {}
        if dict_check and isinstance(input_args[-1], dict):
            input_kwargs = input_args[-1]
            input_args = input_args[:-1]
        try:
            model_copy = copy.deepcopy(model)
            output = model_copy(*input_args, **input_kwargs)
        except Exception:
            output = model(*input_args, **input_kwargs)
        if isinstance(output, torch.Tensor):
            output = (output,)

        if not dict_check and isinstance(input[-1], dict):
            input = input + ({},)

        ort_sess = convert_to_onnx(model, input=input, opset_version=self.opset_version,
                                   do_constant_folding=do_constant_folding,
                                   keep_initializers_as_inputs=self.keep_initializers_as_inputs,
                                   dynamic_axes=dynamic_axes, input_names=input_names,
                                   output_names=output_names, fixed_batch_size=fixed_batch_size, training=training,
                                   onnx_shape_inference=self.onnx_shape_inference)
        # compute onnxruntime output prediction
        if remained_onnx_input_idx is not None:
            input_onnx = []
            for idx in remained_onnx_input_idx:
                input_onnx.append(input[idx])
            input = input_onnx

        input_copy = copy.deepcopy(input)
        if flatten:
            input_copy, _ = torch.jit._flatten(input_copy)

        ort_outs = run_ort(ort_sess, input_copy)
        ort_compare_with_pytorch(ort_outs, output, rtol, atol)


        # if additional test inputs are provided run the onnx
        # model with these inputs and check the outputs
        if test_with_inputs is not None:
            for test_input in test_with_inputs:
                if isinstance(test_input, torch.Tensor):
                    test_input = (test_input,)
                test_input_copy = copy.deepcopy(test_input)
                output = model(*test_input_copy)
                if isinstance(output, torch.Tensor):
                    output = (output,)
                if remained_onnx_input_idx is not None:
                    test_input_onnx = []
                    for idx in remained_onnx_input_idx:
                        test_input_onnx.append(test_input[idx])
                    test_input = test_input_onnx
                if flatten:
                    test_input, _ = torch.jit._flatten(test_input)
                ort_outs = run_ort(ort_sess, test_input)
                ort_compare_with_pytorch(ort_outs, output, rtol, atol)
