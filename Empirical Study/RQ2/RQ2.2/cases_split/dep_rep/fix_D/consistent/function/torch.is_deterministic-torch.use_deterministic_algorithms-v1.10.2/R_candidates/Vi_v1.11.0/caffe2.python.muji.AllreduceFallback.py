def AllreduceFallback(net, blobs, reduced_affix, gpu_indices):
    """A fallback option for Allreduce with no assumption on p2p.

  Algorithm: a flat operation on gpu 0
      0r <- 0
      0r <- 0r + i for i in gpu_indices[1:]
      ir <- 0r for i in gpu_indices[1:]
  """
    reduced = [None] * len(gpu_indices)
    if reduced_affix != '':
        # copy first
        reduced[0] = net.Copy(
            blobs[0],
            blobs[0] + reduced_affix,
            device_option=OnGPU(gpu_indices[0])
        )
    else:
        reduced[0] = blobs[0]
    # do temp copy and add
    temp_name = reduced[0] + '_temp_copy'
    for i in range(1, len(gpu_indices)):
        temp = net.Copy(
            blobs[i],
            temp_name,
            device_option=OnGPU(gpu_indices[0])
        )
        reduced[0] = net.Add(
            [temp, reduced[0]],
            reduced[0],
            device_option=OnGPU(gpu_indices[0])
        )
    # Broadcast to everyone else
    for i in range(1, len(gpu_indices)):
        reduced[i] = net.Copy(
            reduced[0],
            blobs[i] + reduced_affix,
            device_option=OnGPU(gpu_indices[i])
        )
    return reduced
