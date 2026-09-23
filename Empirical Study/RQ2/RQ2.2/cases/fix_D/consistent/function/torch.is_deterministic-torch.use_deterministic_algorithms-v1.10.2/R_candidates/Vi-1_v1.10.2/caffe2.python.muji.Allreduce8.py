def Allreduce8(net, blobs, reduced_affix, gpu_indices):
    """Allreduce for 8 gpus.

  Algorithm: 3 level reduction.
      0r <- 0 + 1, 2r <- 2 + 3, 4r <- 4 + 5, 6r <- 6 + 7
      0r <- 0r + 2r, 4r <- 4r + 6r
      0r <- 0r + 4r
      4r <- 0r
      2r <- 0r, 6r <- 4r
      1r <- 0r, 3r <- 2r, 5r <- 4r, 7r <- 6r
  """
    reduced = [None] * 8
    # Reduction level 1
    for i in [0, 2, 4, 6]:
        reduced[i] = net.Add(
            [blobs[i], blobs[i + 1]],
            blobs[i] + reduced_affix,
            device_option=OnGPU(gpu_indices[i])
        )
    # Reduction level 2
    for i in [0, 4]:
        reduced[i] = net.Add(
            [reduced[i], reduced[i + 2]],
            str(blobs[i]) + reduced_affix,
            device_option=OnGPU(gpu_indices[i])
        )
    # Reduction level 3: this involves a copy.
    reduced_4_copy = reduced[4].Copy(
        [],
        str(reduced[4]) + '_copy',
        device_option=OnGPU(gpu_indices[0])
    )
    reduced[0] = reduced[0].Add(
        reduced_4_copy,
        reduced[0],
        device_option=OnGPU(gpu_indices[0])
    )
    # Broadcast level 1
    reduced[4] = reduced[0].Copy(
        [],
        reduced[4],
        device_option=OnGPU(gpu_indices[4])
    )
    # Broadcast level 2
    for i in [2, 6]:
        reduced[i] = reduced[i - 2].Copy(
            [],
            reduced[i],
            device_option=OnGPU(gpu_indices[i])
        )
    # Broadcast level 3
    for i in [1, 3, 5, 7]:
        reduced[i] = reduced[i - 1].Copy(
            [],
            blobs[i] + reduced_affix,
            device_option=OnGPU(gpu_indices[i])
        )
    return reduced
