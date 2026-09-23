def Allreduce2(net, blobs, reduced_affix, gpu_indices):
    """Allreduce for 2 gpus.

  Algorithm: 0r <- 0 + 1, 1r <- 0r, where r means "reduced"
  """
    a, b = blobs
    gpu_a, gpu_b = gpu_indices
    a_reduced = net.Add([a, b], a + reduced_affix, device_option=OnGPU(gpu_a))
    b_reduced = a_reduced.Copy(
        [],
        b + reduced_affix,
        device_option=OnGPU(gpu_b)
    )
    return a_reduced, b_reduced
