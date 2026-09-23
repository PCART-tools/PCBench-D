def put_remote_code_state(cache_key: str) -> None:
    with dynamo_timed(name := "pgo.put_remote_code_state", log_pt2_compile_event=True):
        CompileEventLogger.pt2_compile(name, cache_key=cache_key)
        assert _CODE_STATE is not None

        remote_cache = get_remote_cache()

        if remote_cache is None:
            log.info("put_code_state: remote cache disabled")
            return

        content = pickle.dumps(_CODE_STATE)
        CompileEventLogger.pt2_compile(name, cache_size_bytes=len(content))
        cache_data: JsonDataTy = {
            "data": base64.b64encode(content).decode("ascii"),
        }
        remote_cache.put(cache_key, cache_data)
        log.info(
            "put_code_state: wrote remote %s, %d entries", cache_key, len(_CODE_STATE)
        )
        # TODO: don't log this multiple times
        trace_structured_artifact(
            "put_remote_code_state",
            "string",
            lambda: render_code_state(_CODE_STATE),
        )
