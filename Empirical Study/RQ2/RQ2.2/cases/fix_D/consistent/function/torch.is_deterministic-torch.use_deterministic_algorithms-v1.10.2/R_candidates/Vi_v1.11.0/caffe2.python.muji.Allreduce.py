def Allreduce(net, blobs, reduced_affix="_reduced", gpu_indices=None):
    """The general Allreduce interface that reroutes the function calls.
    CPUs and AMD GPUs are not supported because
    GetGpuPeerAccessPattern is called to get gpu peer access pattern.
  """
    if gpu_indices is None:
        gpu_indices = list(range(len(blobs)))
    if len(gpu_indices) != len(blobs):
        raise RuntimeError(
            "gpu_indices length and blobs length mismatch: %d vs %d" %
            (len(gpu_indices), len(blobs))
        )
    pattern = workspace.GetGpuPeerAccessPattern()
    if len(blobs) == 2 and pattern.shape[0] >= 2 and np.all(pattern[:2, :2]):
        return Allreduce2(net, blobs, reduced_affix, gpu_indices)
    elif len(blobs) == 4 and pattern.shape[0] >= 4 and np.all(pattern[:4, :4]):
        return Allreduce4(net, blobs, reduced_affix, gpu_indices)
    elif len(blobs) == 4 and pattern.shape[0] >= 4 and np.all(pattern[:2, :2]) and np.all(pattern[2:4, 2:4]):
        return Allreduce4Group2(net, blobs, reduced_affix, gpu_indices)
    elif len(blobs) == 8 and pattern.shape[0] >= 8 and np.all(pattern[:8, :8]):
        return Allreduce8(net, blobs, reduced_affix, gpu_indices)
    else:
        return AllreduceFallback(net, blobs, reduced_affix, gpu_indices)
