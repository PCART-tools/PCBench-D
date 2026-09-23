def config_to_dict(config: Config) -> dict[str, Any]:
    return {
        **config.kwargs,
        "num_warps": config.num_warps,
        "num_stages": config.num_stages,
    }
