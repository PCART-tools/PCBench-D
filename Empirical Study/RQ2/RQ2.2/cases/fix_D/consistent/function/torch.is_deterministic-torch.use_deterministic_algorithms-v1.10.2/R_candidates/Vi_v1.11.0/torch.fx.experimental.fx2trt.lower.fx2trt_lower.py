def fx2trt_lower(module: nn.Module, sample_input: t.Any) -> fx.GraphModule:
    """Lowers the module using fx2trt

    TODO: @kefeilu: this function's body should be moved into the actual calling
    site in the model publisher workflow, since now the lowering function
    signature (`LowerFunc`) is encapsulated in the `Lowerer` callable class.
    """

    assert isinstance(
        module, fx.GraphModule
    ), f"Expecting fx.GraphModule, got: {type(module)}"
    logger.info(f"Module FX Graph: {module.graph}")
    lower_setting = LowerSetting()
    lower = Lowerer.create(lower_setting=lower_setting)

    module_lowered = lower(module, sample_input)

    assert isinstance(module_lowered, fx.GraphModule)
    return module_lowered
