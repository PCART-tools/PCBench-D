def handle_traced_output(example_value, tx, proxy, options, subclass_type, target_cls):
    import torch._functorch.vmap
    import torch._subclasses.fake_tensor
    import torch._utils

    if isinstance(example_value, torch.Tensor):
        var = construct_tensor_variable(
            target_cls, tx, proxy, example_value, subclass_type, options
        )
        # NOTE: [Side effect tracking for newly constructed tensor]
        # For newly constructed objects that have mutable attributes, we usually
        # construct their VariableTracker via `track_object_new`, but since
        # tensor variable construction is a bit different, we handle them
        # specially here. This ensures that codegen will actually generate the
        # attribute mutations on this tensor.
        #
        # NOTE we pass a dummy object as the `item` argument to avoid
        # constructing a dummy _tensor_ object. The object isn't used for
        # newly constructed VTs anyways.
        tx.output.side_effects._track_obj(
            proxy, var, mutation_type_cls=AttributeMutationNew
        )
        return var
    elif (
        hasattr(proxy.node.target, "__name__")
        and proxy.node.target.__name__ == "set_state"
        and isinstance(proxy.node.target.__self__, torch._C.Generator)
        or proxy.node.target == torch.random.set_rng_state
    ):
        return TorchInGraphFunctionVariable(proxy.node.target)
    elif (
        proxy.node.target == torch._C._DisableFuncTorch
        or proxy.node.target == torch.cuda._is_in_bad_fork
    ):
        return UserDefinedObjectVariable(example_value)
    elif istype(example_value, torch.Size) and all(
        isinstance(x, int) for x in example_value
    ):
        sizes = [ConstantVariable.create(x) for x in example_value]
        return SizeVariable(sizes, **options)
    elif isinstance(example_value, (tuple, list)):
        set_example_value(proxy.node, example_value)
        unpacked = []
        for i, val in enumerate(example_value):
            if val is None:
                # nn.MultiheadAttention() can return None, see issue #175
                unpacked.append(
                    ConstantVariable.create(None, **options),
                )
            else:
                proxy_i = proxy.tracer.create_proxy(
                    kind="call_function",
                    target=operator.getitem,
                    args=(proxy, i),
                    kwargs={},
                )

                if "source" in options:
                    # This path should only trigger for list stealing, so it's
                    # safe to use `GetItemSource`.
                    assert isinstance(example_value, list)
                    source = options["source"]
                    options_i = options.copy()
                    options_i["source"] = GetItemSource(
                        base=source, index=i, index_is_slice=False
                    )
                else:
                    # use the same options object as parent
                    options_i = options

                # WARNING: this assumes the same target_cls as this tuple/list call
                unpacked.append(
                    wrap_fx_proxy_cls(
                        target_cls=target_cls,
                        tx=tx,
                        proxy=proxy_i,
                        example_value=val,
                        **options_i,
                    )
                )
        if isinstance(example_value, torch.Size):
            # NB: Keep the old proxy around.  See SizeVariable for an
            # explanation why
            return SizeVariable(unpacked, proxy, **options)
        elif istype(example_value, tuple):
            return TupleVariable(unpacked, **options)
        elif istype(example_value, (list, immutable_list)):
            return ListVariable(unpacked, **options)
        else:
            assert (
                example_value.__class__.__module__ == "torch.return_types"
                or hasattr(example_value, "_fields")
            ), (
                f"expected {example_value.__class__.__module__} == torch.return_types or named tuple but got {type(example_value)}"
            )
            return NamedTupleVariable(unpacked, example_value.__class__, **options)
    elif example_value is None or proxy.node.target is torch.manual_seed:
        return ConstantVariable.create(None, **options)
    elif isinstance(example_value, (torch.SymInt, torch.SymFloat, torch.SymBool)):
        tx.output.current_tracer.track_unbacked_symbols(example_value, proxy)
        set_example_value(proxy.node, example_value)
        return SymNodeVariable(proxy, example_value, **options)
    elif (
        inspect.isclass(proxy.node.target)
        and issubclass(proxy.node.target, torch.Stream)
    ) or proxy.node.target in [
        device_interface.current_stream
        for _, device_interface in get_registered_device_interfaces()
    ]:
        set_example_value(proxy.node, example_value)
        return StreamVariable(proxy, example_value, example_value.device, **options)
    elif (
        inspect.isclass(proxy.node.target)
        and issubclass(proxy.node.target, torch.Event)
    ) or proxy.node.target in [
        device_interface.Event
        for _, device_interface in get_registered_device_interfaces()
    ]:
        set_example_value(proxy.node, example_value)
        return EventVariable(proxy, example_value, **options)
    elif proxy.node.target == "query" and proxy.node.op == "call_method":
        set_example_value(proxy.node, example_value)
        return ConstantVariable(example_value, **options)
    elif (
        example_value is not None
        and isinstance(example_value, torch.Event)
        and proxy.node.target == "record_event"
        and proxy.node.op == "call_method"
    ):
        set_example_value(proxy.node, example_value)
        return EventVariable(proxy, example_value, **options)
    elif isinstance(example_value, int) and (
        proxy.node.target
        in [
            torch.sym_int,
            getattr,
            operator.getitem,
            torch._utils._element_size,
            torch.seed,
            operator.mod,
            torch._functorch.vmap._validate_and_get_batch_size,
            # some mac builds are missing torch.distributed.get_rank()
            getattr(torch.distributed, "get_rank", _missing),
            getattr(torch.distributed, "get_world_size", _missing),
            # This always wants to be in the graph, even if the constraint
            # results in a constant int
            torch._constrain_as_size,
        ]
        or (
            # TODO: this is a little sus, because we didn't check what the self is
            proxy.node.op == "call_method" and proxy.node.target in ["bit_length"]
        )
    ):
        set_example_value(proxy.node, example_value)
        return ConstantVariable.create(example_value, **options)
    elif isinstance(example_value, torch.backends.cuda.SDPAParams):
        from .sdpa import SDPAParamsVariable

        set_example_value(proxy.node, example_value)
        return SDPAParamsVariable(proxy, **options)
    elif isinstance(example_value, bool) and (
        proxy.node.target
        in [
            torch._C._are_functorch_transforms_active,
            torch._C._functorch.is_batchedtensor,
            torch.backends.cuda.is_flash_attention_available,
            torch.backends.cuda.can_use_flash_attention,
            torch.backends.cuda.can_use_efficient_attention,
            "is_integer",
        ]
        + list(supported_const_comparison_op_values.keys())
    ):
        set_example_value(proxy.node, example_value)
        return ConstantVariable.create(example_value, **options)
    elif (
        isinstance(example_value, (int, float, bool))
        and proxy.node.target is call_torchbind
    ):
        set_example_value(proxy.node, example_value)
        return ConstantVariable.create(example_value, **options)
    elif isinstance(example_value, float) or proxy.node.target in ["hex", "__round__"]:
        set_example_value(proxy.node, example_value)
        return ConstantVariable.create(example_value, **options)
    else:
        unimplemented_v2(
            gb_type="torch.* op returned non-Tensor",
            context=f"example_value type: {typestr(example_value)}; op: {proxy.node.op}; target: {proxy.node.target}",
            explanation="torch.* ops that return a non-Tensor cannot be traced into the Dynamo FX graph output",
            hints=[],
        )
