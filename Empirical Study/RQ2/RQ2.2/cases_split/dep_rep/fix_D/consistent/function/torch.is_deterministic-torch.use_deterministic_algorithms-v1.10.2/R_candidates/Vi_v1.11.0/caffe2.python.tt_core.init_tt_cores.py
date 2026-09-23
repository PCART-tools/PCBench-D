def init_tt_cores(inp_sizes, out_sizes, tt_ranks, seed=1234):
    """
    Initialize randomized orthogonalized TT-cores.

    This method should be used when a TT-layer is trained from scratch. The
    sizes of each of the cores are specified by the inp_sizes and out_sizes, and
    the respective tt_ranks will dictate the ranks of each of the cores. Note
    that a larger set of tt_ranks will result in slower computation but will
    result in more accurate approximations. The size of the ith core is:

        tt_ranks[i] * inp_sizes[i] * out_sizes[i] * tt_ranks[i + 1].

    Note that the following relationships of lengths of each input is expected:

        len(inp_sizes) == len(out_sizes) == len(tt_ranks) - 1.

    Args:
        inp_sizes: list of the input dimensions of the respective cores
        out_sizes: list of the output dimensions of the respective cores
        tt_ranks: list of the ranks of the respective cores
        seed: integer to seed the random number generator

    Returns:
        cores: One-dimensional list of cores concatentated along an axis
    """
    np.random.seed(seed)

    # Assert that the sizes of each input is correct
    assert(len(inp_sizes) == len(out_sizes)), \
           "The number of input dimensions (" + str(len(inp_sizes)) + \
           ") must be equal to the number of output dimensions (" + \
           str(len(out_sizes)) + ")."

    assert(len(tt_ranks) == len(inp_sizes) + 1), \
           "The number of tt-ranks (" + str(len(tt_ranks)) + ") must be " + \
           "one more than the number of input and output dims (" + \
           str(len(out_sizes)) + ")."

    # Convert to numpy arrays
    inp_sizes = np.array(inp_sizes)
    out_sizes = np.array(out_sizes)
    tt_ranks = np.array(tt_ranks)

    # Initialize the cores array
    cores_len = np.sum(
        inp_sizes * out_sizes * tt_ranks[1:] * tt_ranks[:-1])
    cores = np.zeros(cores_len)
    cores_idx = 0
    rv = 1

    # Compute the full list of cores by computing each individual one
    for i in range(inp_sizes.shape[0]):
        shape = [tt_ranks[i],
                 inp_sizes[i],
                 out_sizes[i],
                 tt_ranks[i + 1]]

        # Precompute the shape of each core
        tall_shape = (np.prod(shape[:3]), shape[3])

        # Randomly initialize the current core using a normal distribution
        curr_core = np.dot(rv, np.random.normal(
            0, 1, size=(shape[0], np.prod(shape[1:]))))
        curr_core = curr_core.reshape(tall_shape)

        # Orthogonalize the initialized current core and append to cores list
        if i < inp_sizes.shape[0] - 1:
            curr_core, rv = np.linalg.qr(curr_core)
        cores[cores_idx:cores_idx +
              curr_core.size] = curr_core.flatten()
        cores_idx += curr_core.size

    # Normalize the list of arrays using this Glarot trick
    glarot_style = (np.prod(inp_sizes) *
                    np.prod(tt_ranks))**(1.0 / inp_sizes.shape[0])

    return (0.1 / glarot_style) * np.array(cores).astype(np.float32)
