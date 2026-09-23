def get_quant_type() -> torch.dtype:
    quant_type = torch._inductor.config.post_grad_fusion_options[
        "activation_quantization_aten_pass"
    ].get("quant_type", "torch.float8_e5m2")

    return getattr(torch, quant_type.split(".")[-1])
