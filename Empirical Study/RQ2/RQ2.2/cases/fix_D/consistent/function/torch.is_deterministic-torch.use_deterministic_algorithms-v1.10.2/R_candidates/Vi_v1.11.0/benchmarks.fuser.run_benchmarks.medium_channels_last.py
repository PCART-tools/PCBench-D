def medium_channels_last():
    return (
        rand(32, 3, 224, 224).to(memory_format=torch.channels_last),
        rand(32, 3, 224, 224).to(memory_format=torch.channels_last),
    )
