def lstm_unit(*args, **kwargs):
    forget_bias = kwargs.get('forget_bias', 0.0)
    drop_states = kwargs.get('drop_states', False)
    sequence_lengths = kwargs.get('sequence_lengths', True)

    if sequence_lengths:
        hidden_t_prev, cell_t_prev, gates, seq_lengths, timestep = args
    else:
        hidden_t_prev, cell_t_prev, gates, timestep = args
    D = cell_t_prev.shape[2]
    G = gates.shape[2]
    N = gates.shape[1]
    t = (timestep * np.ones(shape=(N, D))).astype(np.int32)
    assert t.shape == (N, D)
    assert G == 4 * D
    # Resize to avoid broadcasting inconsistencies with NumPy
    gates = gates.reshape(N, 4, D)
    cell_t_prev = cell_t_prev.reshape(N, D)
    i_t = gates[:, 0, :].reshape(N, D)
    f_t = gates[:, 1, :].reshape(N, D)
    o_t = gates[:, 2, :].reshape(N, D)
    g_t = gates[:, 3, :].reshape(N, D)
    i_t = sigmoid(i_t)
    f_t = sigmoid(f_t + forget_bias)
    o_t = sigmoid(o_t)
    g_t = tanh(g_t)
    if sequence_lengths:
        seq_lengths = (np.ones(shape=(N, D)) *
                       seq_lengths.reshape(N, 1)).astype(np.int32)
        assert seq_lengths.shape == (N, D)
        valid = (t < seq_lengths).astype(np.int32)
    else:
        valid = np.ones(shape=(N, D))
    assert valid.shape == (N, D)
    cell_t = ((f_t * cell_t_prev) + (i_t * g_t)) * (valid) + \
        (1 - valid) * cell_t_prev * (1 - drop_states)
    assert cell_t.shape == (N, D)
    hidden_t = (o_t * tanh(cell_t)) * valid + hidden_t_prev * (
        1 - valid) * (1 - drop_states)
    hidden_t = hidden_t.reshape(1, N, D)
    cell_t = cell_t.reshape(1, N, D)
    return hidden_t, cell_t
