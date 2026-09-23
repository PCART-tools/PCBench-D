def get_max_alg_id() -> Optional[int]:
    if not _init():
        return None
    return __MAX_ALG_ID
