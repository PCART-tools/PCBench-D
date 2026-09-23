def prepare_qat_fx(
    model: torch.nn.Module,
    qconfig_dict: Any,
    prepare_custom_config_dict: Optional[Dict[str, Any]] = None,
    backend_config_dict: Optional[Dict[str, Any]] = None,
) -> ObservedGraphModule:
    r""" Prepare a model for quantization aware training

    Args:
      * `model`: torch.nn.Module model, must be in train mode
      * `qconfig_dict`: see :func:`~torch.ao.quantization.prepare_fx`
      * `prepare_custom_config_dict`: see :func:`~torch.ao.quantization.prepare_fx`
      * `backend_config_dict`: see :func:`~torch.ao.quantization.prepare_fx`

    Return:
      A GraphModule with fake quant modules (configured by qconfig_dict), ready for
      quantization aware training

    Example::

        import torch
        from torch.ao.quantization import get_default_qat_qconfig
        from torch.ao.quantization import prepare_fx

        qconfig = get_default_qat_qconfig('fbgemm')
        def train_loop(model, train_data):
            model.train()
            for image, target in data_loader:
                ...

        float_model.train()
        qconfig_dict = {"": qconfig}
        prepared_model = prepare_fx(float_model, qconfig_dict)
        # Run calibration
        train_loop(prepared_model, train_loop)

    """
    torch._C._log_api_usage_once("quantization_api.quantize_fx.prepare_qat_fx")
    assert model.training, "prepare_qat_fx only works for models in  " + "train mode"
    return _prepare_fx(
        model,
        qconfig_dict,
        True,  # is_qat
        prepare_custom_config_dict,
        backend_config_dict=backend_config_dict,
    )
