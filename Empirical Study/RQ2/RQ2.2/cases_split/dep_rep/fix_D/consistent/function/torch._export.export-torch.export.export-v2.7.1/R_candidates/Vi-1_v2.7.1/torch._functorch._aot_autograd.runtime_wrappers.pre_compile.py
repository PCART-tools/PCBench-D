def pre_compile(
    wrappers: list[CompilerWrapper],
    flat_fn: Callable,
    flat_args: list[Any],
    aot_config: AOTConfig,
    *,
    fw_metadata: ViewAndMutationMeta,
) -> tuple[Callable, list[Tensor], ViewAndMutationMeta]:
    """
    Runs a sequence of wrappers on the given function and arguments.
    Mutates wrappers in place.
    """
    for wrapper in wrappers:
        flat_fn, flat_args, fw_metadata = wrapper.pre_compile(
            flat_fn, flat_args, aot_config, fw_metadata=fw_metadata
        )
    return flat_fn, flat_args, fw_metadata
