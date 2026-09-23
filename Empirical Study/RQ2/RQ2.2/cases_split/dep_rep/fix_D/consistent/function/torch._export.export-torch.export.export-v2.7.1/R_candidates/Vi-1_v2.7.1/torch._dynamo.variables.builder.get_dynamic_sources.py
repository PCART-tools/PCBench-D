def get_dynamic_sources() -> set[str]:
    global _DYNAMIC_SOURCES
    if _DYNAMIC_SOURCES is not None:
        return _DYNAMIC_SOURCES

    _DYNAMIC_SOURCES = set(
        torch.compiler.config.dynamic_sources.replace(" ", "").split(",")
    )

    return _DYNAMIC_SOURCES
