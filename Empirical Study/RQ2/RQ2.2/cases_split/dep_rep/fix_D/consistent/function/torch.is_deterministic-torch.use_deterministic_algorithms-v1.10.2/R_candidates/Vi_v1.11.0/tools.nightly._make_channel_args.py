def _make_channel_args(
    channels: Iterable[str] = ("pytorch-nightly",),
    override_channels: bool = False,
) -> List[str]:
    args = []
    for channel in channels:
        args.append("--channel")
        args.append(channel)
    if override_channels:
        args.append("--override-channels")
    return args
