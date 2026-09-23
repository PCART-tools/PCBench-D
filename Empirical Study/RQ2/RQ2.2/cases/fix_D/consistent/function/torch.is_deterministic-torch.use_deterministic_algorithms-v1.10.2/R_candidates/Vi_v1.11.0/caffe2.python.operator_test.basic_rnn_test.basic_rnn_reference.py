def basic_rnn_reference(input, hidden_initial,
                        i2h_w, i2h_b,
                        gate_w, gate_b,
                        seq_lengths,
                        drop_states,
                        use_sequence_lengths):
    D = hidden_initial.shape[-1]
    T = input.shape[0]
    N = input.shape[1]

    if seq_lengths is not None:
        seq_lengths = (np.ones(shape=(N, D)) *
                       seq_lengths.reshape(N, 1)).astype(np.int32)

    ret = []

    hidden_prev = hidden_initial

    for t in range(T):
        input_fc = np.dot(input[t], i2h_w.T) + i2h_b
        recur_fc = np.dot(hidden_prev, gate_w.T) + gate_b
        hidden_t = tanh(input_fc + recur_fc)

        if seq_lengths is not None:
            valid = (t < seq_lengths).astype(np.int32)
            assert valid.shape == (N, D), (valid.shape, (N, D))
            hidden_t = hidden_t * valid + \
                       hidden_prev * (1 - valid) * (1 - drop_states)

        ret.append(hidden_t)
        hidden_prev = hidden_t
    return ret
