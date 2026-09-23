def _init_for_cuda_graphs():
    from torch.autograd.profiler import profile

    with profile():
        pass
