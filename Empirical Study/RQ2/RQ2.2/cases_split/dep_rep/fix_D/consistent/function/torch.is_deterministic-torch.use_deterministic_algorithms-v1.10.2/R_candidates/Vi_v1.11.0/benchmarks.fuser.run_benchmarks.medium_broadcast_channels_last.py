def medium_broadcast_channels_last():
    return (rand(32, 3, 223, 223).to(memory_format=torch.channels_last), rand(3, 1, 1))
