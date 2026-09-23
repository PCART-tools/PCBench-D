def _create_delayed_compile_callback(callback, stance):
    def callback_fn(*args, **kwargs):
        frame = args[0]
        example_inputs = _get_or_add_example_inputs(frame)

        if len(example_inputs) == 1:
            if stance == "eager_then_compile":
                return ConvertFrameReturn(
                    frame_exec_strategy=FrameExecStrategy(
                        FrameAction.DEFAULT, FrameAction.DEFAULT
                    )
                )
            elif stance == "aot_eager_then_compile":
                aot_eager_fn = get_compiler_fn("aot_eager")
                return _create_wrapped_callback(aot_eager_fn)(*args, **kwargs)

        dynamism = track_dynamism_across_examples(example_inputs)
        code_context.get_context(frame.f_code)["dynamism"] = dynamism
        compiler_fn = callback._torchdynamo_orig_callable._torchdynamo_orig_callable
        return _create_wrapped_callback(compiler_fn)(*args, **kwargs)

    return callback_fn
