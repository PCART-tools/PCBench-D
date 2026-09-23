    @lru_cache(None)
    def get_zoneinfo(key: str) -> ZoneInfo:  # noqa: D103
        return zoneinfo.ZoneInfo(key)
