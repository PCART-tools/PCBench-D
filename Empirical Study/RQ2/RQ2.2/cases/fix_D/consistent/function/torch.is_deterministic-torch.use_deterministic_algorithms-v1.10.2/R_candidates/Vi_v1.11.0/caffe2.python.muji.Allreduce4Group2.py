def Allreduce4Group2(net, blobs, reduced_affix, gpu_indices):
    """Allreduce for 4 gpus where peer access are enabled in {0,1} and {2,3}

  Algorithm: 2 level reduction.
      0r <- 0 + 1, 2r <- 2 + 3
      0r <- 0r + 2r
      2r <- 0r,
      1r <- 0r, 3r <- 2r
  """
    a, b, c, d = blobs
    gpu_a, gpu_b, gpu_c, gpu_d = gpu_indices
    # a_reduced <- a+b, c_reduced <- c + d
    a_reduced = net.Add(
        [a, b],
        str(a) + reduced_affix,
        device_option=OnGPU(gpu_a)
    )
    c_reduced = net.Add(
        [c, d],
        str(c) + reduced_affix,
        device_option=OnGPU(gpu_c)
    )
    # copy from c_reduce(gpu_c) to c_reduce_copy(gpu_a)
    c_reduced_copy = c_reduced.Copy(
        [],
        str(c_reduced) + '_copy',
        device_option=OnGPU(gpu_a)
    )
    # a_reduced <- a_reduced + c_reduced_copy
    a_reduced = a_reduced.Add(c_reduced_copy, a_reduced, device_option=OnGPU(gpu_a))
    # broadcast a_reduced to c_reduced
    c_reduced = a_reduced.Copy([], c_reduced, device_option=OnGPU(gpu_c))
    # broadcast to b and d
    b_reduced = a_reduced.Copy(
        [],
        str(b) + reduced_affix,
        device_option=OnGPU(gpu_b)
    )
    d_reduced = c_reduced.Copy(
        [],
        str(d) + reduced_affix,
        device_option=OnGPU(gpu_d)
    )
    return a_reduced, b_reduced, c_reduced, d_reduced
