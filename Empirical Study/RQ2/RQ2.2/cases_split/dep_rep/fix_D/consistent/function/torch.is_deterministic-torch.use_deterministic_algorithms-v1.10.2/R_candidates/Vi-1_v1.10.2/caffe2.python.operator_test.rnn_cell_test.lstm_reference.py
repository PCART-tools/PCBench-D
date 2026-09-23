def lstm_reference(input, hidden_input, cell_input,
                   gates_w, gates_b, seq_lengths, forget_bias,
                   drop_states=False):
    T = input.shape[0]
    N = input.shape[1]
    G = input.shape[2]
    D = hidden_input.shape[hidden_input.ndim - 1]
    hidden = np.zeros(shape=(T + 1, N, D))
    cell = np.zeros(shape=(T + 1, N, D))
    assert hidden.shape[0] == T + 1
    assert cell.shape[0] == T + 1
    assert hidden.shape[1] == N
    assert cell.shape[1] == N
    cell[0, :, :] = cell_input
    hidden[0, :, :] = hidden_input
    for t in range(T):
        input_t = input[t].reshape(1, N, G)
        hidden_t_prev = hidden[t].reshape(1, N, D)
        cell_t_prev = cell[t].reshape(1, N, D)
        gates = np.dot(hidden_t_prev, gates_w.T) + gates_b
        gates = gates + input_t
        hidden_t, cell_t = lstm_unit(
            hidden_t_prev,
            cell_t_prev,
            gates,
            seq_lengths,
            t,
            forget_bias=forget_bias,
            drop_states=drop_states,
        )
        hidden[t + 1] = hidden_t
        cell[t + 1] = cell_t
    return (
        hidden[1:],
        hidden[-1].reshape(1, N, D),
        cell[1:],
        cell[-1].reshape(1, N, D)
    )
