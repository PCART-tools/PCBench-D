def nhwc(t):
    t = t.clone().contiguous(memory_format=torch.channels_last)
    t.nnapi_nhwc = True
    return t
