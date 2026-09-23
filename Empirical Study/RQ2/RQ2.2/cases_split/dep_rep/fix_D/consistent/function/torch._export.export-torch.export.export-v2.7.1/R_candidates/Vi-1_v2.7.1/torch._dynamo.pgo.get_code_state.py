def get_code_state() -> defaultdict[CodeId, CodeState]:
    global _CODE_STATE, _INIT_CODE_STATE
    if _CODE_STATE is not None:
        return _CODE_STATE

    # Initialize it (even if we don't look up profile)
    _CODE_STATE = defaultdict(CodeState)

    cache_key = get_cache_key()
    if cache_key is None:
        return _CODE_STATE

    def hit(ty: str) -> defaultdict[CodeId, CodeState]:
        global _INIT_CODE_STATE
        assert isinstance(_CODE_STATE, defaultdict)
        log.info("get_code_state %s hit %s, %d entries", path, ty, len(_CODE_STATE))
        trace_structured_artifact(
            f"get_{ty}_code_state",
            "string",
            lambda: render_code_state(_CODE_STATE),
        )
        set_feature_use("pgo", True)
        _INIT_CODE_STATE = copy.deepcopy(_CODE_STATE)
        return _CODE_STATE

    # Attempt local
    path = code_state_path(cache_key)
    if path is not None and os.path.exists(path):
        with dynamo_timed(
            name := "pgo.get_local_code_state", log_pt2_compile_event=True
        ):
            CompileEventLogger.pt2_compile(name, cache_key=cache_key)
            # Read lock not necessary as we always write atomically write to
            # the actual location
            with open(path, "rb") as f:
                try:
                    content = f.read()
                    _CODE_STATE = pickle.loads(content)
                    CompileEventLogger.pt2_compile(name, cache_size_bytes=f.tell())
                except Exception:
                    log.warning(
                        "get_code_state failed while reading %s", path, exc_info=True
                    )
                else:
                    CacheArtifactManager.record_artifact(
                        CacheArtifactType.PGO, cache_key, content
                    )
                    return hit("local")

    # Attempt remote
    remote_cache = get_remote_cache()
    if remote_cache is not None:
        with dynamo_timed(
            name := "pgo.get_remote_code_state", log_pt2_compile_event=True
        ):
            CompileEventLogger.pt2_compile(name, cache_key=cache_key)
            # TODO: I don't really understand why there's a JSON container format
            try:
                cache_data = remote_cache.get(cache_key)
            except Exception:
                log.warning(
                    "get_code_state failed remote read on %s", cache_key, exc_info=True
                )
            else:
                if cache_data is not None:
                    try:
                        assert isinstance(cache_data, dict)
                        data = cache_data["data"]
                        assert isinstance(data, str)
                        payload = base64.b64decode(data)
                        CompileEventLogger.pt2_compile(
                            name, cache_size_bytes=len(payload)
                        )
                        _CODE_STATE = pickle.loads(payload)
                    except Exception:
                        log.warning(
                            "get_code_state failed parsing remote result on %s",
                            cache_key,
                            exc_info=True,
                        )
                    else:
                        CacheArtifactManager.record_artifact(
                            CacheArtifactType.PGO, cache_key, payload
                        )
                        return hit("remote")
                else:
                    log.info("get_code_state remote miss on %s", cache_key)

    log.info("get_code_state using default")

    assert _CODE_STATE is not None
    return _CODE_STATE
