def create_aot_dispatcher_function(
    flat_fn,
    fake_flat_args: FakifiedFlatArgs,
    aot_config: AOTConfig,
    fake_mode: FakeTensorMode,
    shape_env: Optional[ShapeEnv],
) -> tuple[Callable, ViewAndMutationMeta]:
    with dynamo_timed("create_aot_dispatcher_function", log_pt2_compile_event=True):
        return _create_aot_dispatcher_function(
            flat_fn, fake_flat_args, aot_config, fake_mode, shape_env
        )
