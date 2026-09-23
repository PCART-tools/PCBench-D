    def trace(
        fn_src: str,
        example_tensors: dict[str, CutlassTensor],
        accum_type: DataType,
        output_type: DataType,
        tile_description: TileDescription,
        epilogue_schedule: EpilogueScheduleType,
        name_to_buffer: dict[str, Buffer],
        size_hint_fn: Callable[[Union[Expr, int]], int],
        **kwargs: dict[str, Any],
    ) -> tuple[str, str, str]:
        cuda_arch = int(cuda_env.get_cuda_arch())  # type: ignore[arg-type]
        assert cuda_arch >= 90, "Only SM90+ is supported for EVT"
        epilogue_functor = _trace(fn_src, example_tensors, cuda_arch, **kwargs)
        visitor = EpilogueFunctorVisitor(cuda_arch, epilogue_functor)
        fusion_callbacks = FusionCallbacks(visitor.graph, cuda_arch, emit_CD=False)
        collective_epilogue = CollectiveEpilogue(
            tile_description,
            epilogue_schedule,
            accum_type,
            output_type,
            fusion_callbacks,
        )
        evt_name, evt_code = collective_epilogue.emit()
        evt_args = _render_argument_type(epilogue_functor, name_to_buffer, size_hint_fn)
        return evt_name, evt_args, evt_code
