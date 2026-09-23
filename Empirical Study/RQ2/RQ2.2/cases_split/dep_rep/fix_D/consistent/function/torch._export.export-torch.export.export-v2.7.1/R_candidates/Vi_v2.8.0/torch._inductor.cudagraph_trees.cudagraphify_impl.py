def cudagraphify_impl(
    model: ModelType,
    inputs: list[InputType],
    static_input_idxs: Sequence[int],
    *args: Any,
    **kwargs: Any,
) -> ModelType:
    fn_cache: dict[tuple[int, ...], Callable[..., Any]] = {}

    # Detect int inputs: we need to index on these
    int_key = [i for i, v in enumerate(inputs) if isinstance(v, int)]
    get_ints: Any = operator.itemgetter(*int_key) if int_key else lambda _: None

    has_warn = False

    del inputs

    def deferred_cudagraphify(inputs: list[InputType]) -> OutputType:
        nonlocal has_warn

        int_key = get_ints(inputs)

        if not is_cudagraph_capture_sizes(int_key):
            return model(inputs)

        fn = fn_cache.get(int_key)
        if fn is not None:
            return fn(inputs)

        if int_key is None:
            log.info("recording cudagraph tree for graph without symints")
        else:
            log.info("recording cudagraph tree for symint key %s", int_key)

        if not has_warn:
            has_warn = maybe_warning_due_to_dynamic_shape(fn_cache, int_key)

        # first get indices we need to check to align, then update our static inputs,
        # and finally copy
        check_input_idxs = get_input_idxs_to_check(inputs, static_input_idxs)
        new_static_input_idxs = remove_unaligned_input_idxs(inputs, static_input_idxs)
        copy_misaligned_inputs(inputs, check_input_idxs)

        fn, out = cudagraphify(model, inputs, new_static_input_idxs, *args, **kwargs)
        # cudagraph will already clones input locally, no need to copy back
        mutated_input_idxs: OrderedSet[int] = OrderedSet()
        fn = align_inputs_from_check_idxs(
            fn, inputs_to_check=check_input_idxs, mutated_input_idxs=mutated_input_idxs
        )
        fn_cache[int_key] = fn

        return out

    return deferred_cudagraphify
