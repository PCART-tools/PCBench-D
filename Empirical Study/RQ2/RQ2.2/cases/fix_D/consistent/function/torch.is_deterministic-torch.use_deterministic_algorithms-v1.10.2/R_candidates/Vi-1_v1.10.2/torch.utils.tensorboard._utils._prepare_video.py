def _prepare_video(V):
    """
    Converts a 5D tensor [batchsize, time(frame), channel(color), height, width]
    into 4D tensor with dimension [time(frame), new_width, new_height, channel].
    A batch of images are spreaded to a grid, which forms a frame.
    e.g. Video with batchsize 16 will have a 4x4 grid.
    """
    b, t, c, h, w = V.shape

    if V.dtype == np.uint8:
        V = np.float32(V) / 255.

    def is_power2(num):
        return num != 0 and ((num & (num - 1)) == 0)

    # pad to nearest power of 2, all at once
    if not is_power2(V.shape[0]):
        len_addition = int(2**V.shape[0].bit_length() - V.shape[0])
        V = np.concatenate(
            (V, np.zeros(shape=(len_addition, t, c, h, w))), axis=0)

    n_rows = 2**((b.bit_length() - 1) // 2)
    n_cols = V.shape[0] // n_rows

    V = np.reshape(V, newshape=(n_rows, n_cols, t, c, h, w))
    V = np.transpose(V, axes=(2, 0, 4, 1, 5, 3))
    V = np.reshape(V, newshape=(t, n_rows * h, n_cols * w, c))

    return V
