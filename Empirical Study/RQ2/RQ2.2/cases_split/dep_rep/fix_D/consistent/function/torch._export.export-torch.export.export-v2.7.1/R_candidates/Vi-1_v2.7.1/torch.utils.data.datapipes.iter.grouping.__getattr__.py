def __getattr__(name: str):
    if name in ["SHARDING_PRIORITIES", "ShardingFilterIterDataPipe"]:
        warnings.warn(
            f"`{name}` from `torch.utils.data.datapipes.iter.grouping` is going to be removed in PyTorch 2.1"
            f"Please use `{name}` from the `torch.utils.data.datapipes.iter.sharding`",
            category=FutureWarning,
            stacklevel=2,
        )

        return getattr(torch.utils.data.datapipes.iter.sharding, name)

    raise AttributeError(f"module {__name__} has no attribute {name}")
