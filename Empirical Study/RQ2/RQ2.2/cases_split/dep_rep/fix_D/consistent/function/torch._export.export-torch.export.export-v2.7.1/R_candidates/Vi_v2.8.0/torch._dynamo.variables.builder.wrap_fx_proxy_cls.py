def wrap_fx_proxy_cls(
    target_cls, tx, proxy, example_value=None, subclass_type=None, **options
):
    if example_value is None:
        return _wrap_fx_proxy(
            target_cls, tx, proxy, example_value, subclass_type, **options
        )
    elif isinstance(example_value, torch.Tensor):
        return _wrap_fx_preexisting_tensor(
            target_cls, tx, proxy, example_value, subclass_type, **options
        )
    else:
        # This will skip tracing an op and recursively reinvoke wrap_fx_proxy_cls on supported
        # data structures. In essence this just handles tracing some other value which may
        # contain Fake Tensors or is otherwise proxyable.
        return handle_traced_output(
            example_value, tx, proxy, options, subclass_type, target_cls
        )
