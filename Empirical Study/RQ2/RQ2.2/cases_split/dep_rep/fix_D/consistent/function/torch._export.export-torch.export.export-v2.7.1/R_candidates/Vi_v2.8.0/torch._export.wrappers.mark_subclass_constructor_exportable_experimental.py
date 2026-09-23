def mark_subclass_constructor_exportable_experimental(constructor_subclass):
    """
    Experimental decorator that makes subclass to be traceable in export
    with pre-dispatch IR. To make your subclass traceble in export, you need to:
        1. Implement __init__ method for your subclass (Look at DTensor implementation)
        2. Decorate your __init__ method with _mark_constructor_exportable_experimental
        3. Put torch._dynamo_disable decorator to prevent dynamo from peeking into its' impl

    Example:

    class FooTensor(torch.Tensor):
        @staticmethod
        def __new__(cls, elem, *, requires_grad=False):
            # ...
            return torch.Tensor._make_subclass(cls, elem, requires_grad=requires_grad)

        @torch._dynamo_disable
        @mark_subclass_constructor_exportable_experimental
        def __init__(self, elem, ...):
            # ...
    """

    def _is_init(fn):
        return callable(fn) and fn.__name__ == "__init__"

    if not _is_init(constructor_subclass):
        raise RuntimeError(
            f"torch._export.wrappers.mark_constructor_exportable_experimental can only be applied on subclass tensor.__init__"
            f"But, you are adding it on {constructor_subclass.__name__} which is not supported. "
            f"If __init__ doesn't exist on your subclass, please add it. Look at DTensor.__init__ implementation for example"
        )

    def wrapper(*args, **kwargs):
        if not is_traceable_wrapper_subclass_type(type(args[0])):
            assert constructor_subclass.__qualname__.endswith("__init__")
            obj_name = constructor_subclass.__qualname__[: -len("__init__")]
            raise RuntimeError(
                f"Applying mark_constructor_exportable_experimental on {obj_name} is not valid as it is not a traceable "
                f"tensor subclass. Please look at DTensor.__init__ implementation as an example of proper usage of this API."
            )
        constructor_subclass(*args, **kwargs)
        if not torch._C._is_torch_function_mode_enabled():
            return
        torch_function_mode_stack = torch.overrides._get_current_function_mode_stack()

        pre_dispatch_tf_modes = [
            mode
            for mode in torch_function_mode_stack
            if isinstance(mode, PreDispatchTorchFunctionMode)
        ]
        assert (
            len(pre_dispatch_tf_modes) <= 1
        ), f"Expected only one PreDispatchTorchFunctionMode, found {len(pre_dispatch_tf_modes)}"

        if len(pre_dispatch_tf_modes) == 0:
            return

        mode = pre_dispatch_tf_modes[0]

        tracer = mode.tracer
        subclass = args[0]

        flat_args, in_spec = to_graphable((tuple(args[1:]), kwargs))

        constructor_spec_name = "_".join(
            constructor_subclass.__qualname__.lower().split(".")
        )
        qualname = tracer.get_fresh_qualname(constructor_spec_name)  # type: ignore[union-attr]
        setattr(tracer.root, qualname, in_spec)  # type: ignore[union-attr]
        spec_proxy = tracer.create_proxy("get_attr", qualname, (), {})
        flat_proxy_args = pytree.tree_map_only(
            torch.Tensor, lambda x: get_proxy_slot(x, tracer).proxy, flat_args
        )

        _, func_spec = torch.utils._pytree.tree_flatten(
            _ConstantFunction(type(subclass))
        )

        # We actually don't want to create a new spec for each instance
        # In fx graph, it will look like dtensor_const_func_spec
        # We can't directly shove DTensor.__init__ into fx as it is not
        # allowed type.
        fxable_constructor_call_spec_name = (
            type(subclass).__name__.lower() + "_const_func_spec"
        )

        # We should try to reuse the constructor call spec as it is guaranteed to be same
        # for each subclass type. This is different from proxy-ing the init arguments which
        # can't be reused because for example, DTensor can receive different DeviceMesh etc
        # as it's arguments
        func_spec_proxy = _register_subclass_spec_proxy_in_tracer(
            tracer, fxable_constructor_call_spec_name, func_spec
        )

        inner_proxy = tracer.create_proxy(
            "call_function",
            flat_apply,
            (func_spec_proxy, spec_proxy, *flat_proxy_args),
            {},
        )
        track_tensor_tree(subclass, inner_proxy, constant=None, tracer=tracer)
        return

    return wrapper
