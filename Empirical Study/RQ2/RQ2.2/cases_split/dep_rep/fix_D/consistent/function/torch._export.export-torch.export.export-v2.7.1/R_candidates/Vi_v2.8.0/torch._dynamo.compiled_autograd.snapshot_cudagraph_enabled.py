def snapshot_cudagraph_enabled():
    return torch._inductor.config.triton.cudagraphs
