def reset() -> None:
    """
    Clear all compile caches and restore initial state.  This function is intended
    to reset Dynamo's state *as if* you had started a fresh process invocation, which
    makes it good for testing scenarios where you want to behave as if you started
    a new process.  It does NOT affect any file system caches.

    NB: this does NOT reset logging state.  Don't use this to test logging
    initialization/reinitialization.
    """
    # TODO: https://github.com/pytorch/pytorch/issues/139200
    import logging

    log = logging.getLogger(__name__)
    log.info("torch._dynamo.reset")
    with convert_frame.compile_lock:
        reset_code_caches()
        convert_frame.input_codes.clear()
        reset_code_state()
        convert_frame.output_codes.clear()
        orig_code_map.clear()
        guard_failures.clear()
        graph_break_reasons.clear()
        resume_execution.ContinueExecutionCache.cache.clear()
        _reset_guarded_backend_cache()
        reset_frame_count()
        torch._dynamo.compiled_autograd.reset()
        convert_frame.FRAME_COUNTER = 0
        convert_frame.FRAME_COMPILE_COUNTER.clear()
        callback_handler.clear()
        GenerationTracker.clear()
        TensorifyState.clear()
        torch._dynamo.utils.warn_once_cache.clear()
        torch._dynamo.utils.user_obj_id_to_weakref.clear()
        torch._C._autograd._saved_tensors_hooks_set_tracing(False)
