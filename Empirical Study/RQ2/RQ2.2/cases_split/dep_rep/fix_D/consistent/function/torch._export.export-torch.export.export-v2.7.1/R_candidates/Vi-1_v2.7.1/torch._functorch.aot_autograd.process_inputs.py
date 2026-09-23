def process_inputs(
    flat_args: list[Any],
    aot_config: AOTConfig,
    fake_mode: FakeTensorMode,
    shape_env: Optional[ShapeEnv],
) -> FakifiedFlatArgs:
    with fake_mode:

        def convert(idx, x):
            if shape_env is not None:
                from torch._dynamo.source import ConstantSource

                if isinstance(x, int):
                    # We always specialize on scalar values in export.
                    if aot_config.is_export:
                        return x
                    source = ConstantSource(f"sym_{idx}")
                    return shape_env.create_symintnode(
                        shape_env.create_symbol(x, source), hint=x, source=source
                    )
            if isinstance(x, torch.ScriptObject):
                return torch._library.fake_class_registry.maybe_to_fake_obj(
                    fake_mode, x
                )
            if not isinstance(x, torch.Tensor):
                return x
            if isinstance(x, FakeTensor):
                assert x.fake_mode is fake_mode
                return x
            if is_traceable_wrapper_subclass(x):
                attrs, _ = x.__tensor_flatten__()
                if all(isinstance(getattr(x, attr), FakeTensor) for attr in attrs):
                    assert all(
                        getattr(x, attr).fake_mode is fake_mode for attr in attrs
                    )
                    return x

            # see note [Tensor Fakification and Symbol Caching]
            symbolic_context = None
            source = None
            trace = True
            if tracing_context := torch._guards.TracingContext.try_get():
                if x in tracing_context.tensor_to_context:
                    symbolic_context = tracing_context.tensor_to_context[x]
                    source = symbolic_context.tensor_source
                    # We already fakeified this tensor in Dynamo, don't
                    # dump the trace for it again
                    trace = False
            if (
                idx < aot_config.num_params_buffers
                and config.static_weight_shapes
                and not symbolic_context
            ):
                # TODO: Ensure that this codepath is never exercised from
                # Dynamo
                return fake_mode.from_tensor(x, static_shapes=True)

            return fake_mode.from_tensor(
                x,
                static_shapes=False,
                symbolic_context=symbolic_context,
                source=source,
                trace=trace,
            )

        return FakifiedFlatArgs([convert(idx, x) for idx, x in enumerate(flat_args)])
