def gru_unit(*args, **kwargs):
    '''
    Implements one GRU unit, for one time step

    Shapes:
    hidden_t_prev.shape     = (1, N, D)
    gates_out_t.shape       = (1, N, G)
    seq_lenths.shape        = (N,)
    '''

    drop_states = kwargs.get('drop_states', False)
    sequence_lengths = kwargs.get('sequence_lengths', True)

    if sequence_lengths:
        hidden_t_prev, gates_out_t, seq_lengths, timestep = args
    else:
        hidden_t_prev, gates_out_t, timestep = args

    N = hidden_t_prev.shape[1]
    D = hidden_t_prev.shape[2]
    G = gates_out_t.shape[2]
    t = (timestep * np.ones(shape=(N, D))).astype(np.int32)
    assert t.shape == (N, D)
    assert G == 3 * D
    # Calculate reset, update, and output gates separately
    # because output gate depends on reset gate.
    gates_out_t = gates_out_t.reshape(N, 3, D)
    reset_gate_t = gates_out_t[:, 0, :].reshape(N, D)
    update_gate_t = gates_out_t[:, 1, :].reshape(N, D)
    output_gate_t = gates_out_t[:, 2, :].reshape(N, D)

    # Calculate gate outputs.
    reset_gate_t = sigmoid(reset_gate_t)
    update_gate_t = sigmoid(update_gate_t)
    output_gate_t = tanh(output_gate_t)

    if sequence_lengths:
        seq_lengths = (np.ones(shape=(N, D)) *
                       seq_lengths.reshape(N, 1)).astype(np.int32)
        assert seq_lengths.shape == (N, D)
        valid = (t < seq_lengths).astype(np.int32)
    else:
        valid = np.ones(shape=(N, D))
    assert valid.shape == (N, D)
    hidden_t = update_gate_t * hidden_t_prev + \
        (1 - update_gate_t) * output_gate_t
    hidden_t = hidden_t * valid + hidden_t_prev * \
        (1 - valid) * (1 - drop_states)
    hidden_t = hidden_t.reshape(1, N, D)

    return (hidden_t, )
