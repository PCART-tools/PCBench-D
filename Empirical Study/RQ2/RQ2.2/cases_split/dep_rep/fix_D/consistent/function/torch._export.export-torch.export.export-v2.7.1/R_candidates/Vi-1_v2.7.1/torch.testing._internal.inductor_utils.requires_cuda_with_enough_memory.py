def requires_cuda_with_enough_memory(min_mem_required):
    def inner(fn):
        if not torch.cuda.is_available() or torch.cuda.get_device_properties().total_memory < min_mem_required:
            return unittest.skip(f"Only if the CUDA device has at least {min_mem_required / 1e9:.3f}GB memory to be safe")(fn)
        else:
            return fn

    return inner
