def matrix_to_tt(W, inp_sizes, out_sizes, tt_ranks):
    """
    Convert a matrix into the TT-format.

    This method will consume a 2D weight matrix such as those used in fully
    connected layers in a neural network and will compute the TT-decomposition
    of the weight matrix and return the TT-cores of the resulting computation.
    This method should be used when converting a trained, fully connected layer,
    into a TT-layer for increased speed and decreased parameter size. The size
    of the ith core is:

        tt_ranks[i] * inp_sizes[i] * out_sizes[i] * tt_ranks[i + 1].

    Note that the following relationships of lengths of each input is expected:

        len(inp_sizes) == len(out_sizes) == len(tt_ranks) - 1.

    We also require that np.prod(inp_sizes) == W.shape[0] and that
    np.prod(out_sizes) == W.shape[1].

    Args:
        W: two-dimensional weight matrix numpy array representing a fully
           connected layer to be converted to TT-format; note that the weight
           matrix is transposed before decomposed because we want to emulate the
           X * W^T operation that the FC layer performs.
        inp_sizes: list of the input dimensions of the respective cores
        out_sizes: list of the output dimensions of the respective cores
        tt_ranks: list of the ranks of the respective cores

    Returns:
        new_cores: One-dimensional list of cores concatentated along an axis
   """

    # Assert that the sizes of each input is correct
    assert(len(inp_sizes) == len(out_sizes)), \
           "The number of input dimensions (" + str(len(inp_sizes)) + \
           ") must be equal to the number of output dimensions (" + \
           str(len(out_sizes)) + ")."

    assert(len(tt_ranks) == len(inp_sizes) + 1), \
           "The number of tt-ranks (" + str(len(tt_ranks)) + ") must be " + \
           "one more than the number of input and output dimensions (" + \
           str(len(out_sizes)) + ")."

    assert(W.shape[0] == np.prod(inp_sizes)), \
           "The product of the input sizes (" + str(np.prod(inp_sizes)) + \
           ") must be equal to first dimension of W (" + str(W.shape[0]) + ")."

    assert(W.shape[1] == np.prod(out_sizes)), \
           "The product of the output sizes (" + str(np.prod(out_sizes)) + \
           ") must be equal to second dimension of W (" + str(W.shape[1]) + ")."

    # W is transposed so that the multiplication X * W^T can be computed, just
    # as it is in the FC layer.
    W = W.transpose()

    # Convert to numpy arrays
    inp_sizes = np.array(inp_sizes)
    out_sizes = np.array(out_sizes)
    tt_ranks = np.array(tt_ranks)

    # Copy the original weight matrix in order to permute and reshape the weight
    # matrix. In addition, the inp_sizes and out_sizes are combined to a single
    # sizes array to use the tt_svd helper method, which only consumes a single
    # sizes array.
    W_copy = W.copy()
    total_inp_size = inp_sizes.size
    W_copy = np.reshape(W_copy, np.concatenate((inp_sizes, out_sizes)))
    order = np.repeat(np.arange(0, total_inp_size), 2) + \
            np.tile([0, total_inp_size], total_inp_size)
    W_copy = np.transpose(W_copy, axes=order)
    W_copy = np.reshape(W_copy, inp_sizes * out_sizes)

    # Use helper method to convert the W matrix copy into the preliminary
    # cores array.
    cores = tt_svd(W_copy, inp_sizes * out_sizes, tt_ranks)

    # Permute the dimensions of each of the cores to be compatible with the
    # TT-layer.
    new_cores = np.zeros(cores.shape).astype(np.float32)
    idx = 0
    for i in range(len(inp_sizes)):
        shape = (tt_ranks[i], inp_sizes[i], out_sizes[i], tt_ranks[i + 1])
        current_core = cores[idx:idx + np.prod(shape)].reshape(shape)
        current_core = current_core.transpose((1, 3, 0, 2))
        new_cores[new_cores.shape[0] - idx - np.prod(shape):
                  new_cores.shape[0] - idx] \
                  = current_core.flatten()
        idx += np.prod(shape)

    return new_cores
