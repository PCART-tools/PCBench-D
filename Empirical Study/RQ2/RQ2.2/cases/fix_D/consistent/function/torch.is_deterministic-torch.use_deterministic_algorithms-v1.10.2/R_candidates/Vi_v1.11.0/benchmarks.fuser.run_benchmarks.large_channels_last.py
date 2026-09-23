def large_channels_last():
    return (
        rand(32, 32, 256, 256).to(memory_format=torch.channels_last),
        rand(32, 32, 256, 256).to(memory_format=torch.channels_last),
    )
