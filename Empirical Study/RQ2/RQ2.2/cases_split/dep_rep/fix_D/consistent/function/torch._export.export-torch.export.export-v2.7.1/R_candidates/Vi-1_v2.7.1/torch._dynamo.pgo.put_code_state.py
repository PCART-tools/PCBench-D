def put_code_state() -> None:
    if _CODE_STATE is None:
        log.info("put_code_state: never initialized, will not write")
        return

    if _CODE_STATE == _INIT_CODE_STATE:
        log.info("put_code_state: no change, skipping")
        return

    cache_key = get_cache_key()
    if cache_key is None:
        log.info("put_code_state: no cache key, skipping")
        return

    put_local_code_state(cache_key)
    put_remote_code_state(cache_key)
