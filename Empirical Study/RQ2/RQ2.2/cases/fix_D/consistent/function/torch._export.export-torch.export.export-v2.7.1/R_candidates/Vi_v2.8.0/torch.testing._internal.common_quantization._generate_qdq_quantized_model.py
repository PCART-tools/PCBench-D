def _generate_qdq_quantized_model(
    mod, inputs, is_qat=False, is_dynamic=False, quantizer=None
):
    def get_default_quantizer(is_qat, is_dynamic, inputs):
        has_xpu = any(
            isinstance(input, torch.Tensor) and input.device.type == "xpu"
            for input in inputs
        )
        if has_xpu:
            quantizer = XPUInductorQuantizer()
            assert (not is_qat) and (
                not is_dynamic
            ), "QAT and dynamic quantization is not supported at XPU backend currently"
            quantizer.set_global(xpuiq.get_default_xpu_inductor_quantization_config())
        else:
            quantizer = X86InductorQuantizer()
            quantizer.set_global(
                xiq.get_default_x86_inductor_quantization_config(
                    is_qat=is_qat, is_dynamic=is_dynamic
                )
            )
        return quantizer

    maybe_no_grad = contextlib.nullcontext() if is_qat else torch.no_grad()
    with maybe_no_grad:
        export_model = export_for_training(mod, inputs, strict=True).module()
        quantizer = (
            quantizer
            if quantizer
            else get_default_quantizer(is_qat, is_dynamic, inputs)
        )
        prepare_model = (
            prepare_qat_pt2e(export_model, quantizer)
            if is_qat
            else prepare_pt2e(export_model, quantizer)
        )
        prepare_model(*inputs)
        torch.ao.quantization.move_exported_model_to_eval(prepare_model)
        convert_model = convert_pt2e(prepare_model)
        return convert_model
