def wrap_fx_proxy(
    tx, proxy, example_value=None, subclass_type=None, **options
) -> VariableTracker:
    kwargs = {
        "tx": tx,
        "proxy": proxy,
        "example_value": example_value,
        "subclass_type": subclass_type,
        **options,
    }
    if subclass_type is None:
        return wrap_fx_proxy_cls(target_cls=TensorVariable, **kwargs)
    else:
        result = wrap_fx_proxy_cls(target_cls=TensorWithTFOverrideVariable, **kwargs)
        result.install_global(tx)
        return result
