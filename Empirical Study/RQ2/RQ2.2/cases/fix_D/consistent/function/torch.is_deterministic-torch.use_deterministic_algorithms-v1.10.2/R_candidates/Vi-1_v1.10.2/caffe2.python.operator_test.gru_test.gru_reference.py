def gru_reference(input, hidden_input,
                  reset_gate_w, reset_gate_b,
                  update_gate_w, update_gate_b,
                  output_gate_w, output_gate_b,
                  seq_lengths, drop_states=False,
                  linear_before_reset=False):
    D = hidden_input.shape[hidden_input.ndim - 1]
    T = input.shape[0]
    N = input.shape[1]
    G = input.shape[2]
    print("Dimensions: T= ", T, " N= ", N, " G= ", G, " D= ", D)
    hidden = np.zeros(shape=(T + 1, N, D))
    hidden[0, :, :] = hidden_input

    for t in range(T):
        input_t = input[t].reshape(1, N, G)
        hidden_t_prev = hidden[t].reshape(1, N, D)

        # Split input contributions for three gates.
        input_t = input_t.reshape(N, 3, D)
        input_reset = input_t[:, 0, :].reshape(N, D)
        input_update = input_t[:, 1, :].reshape(N, D)
        input_output = input_t[:, 2, :].reshape(N, D)

        reset_gate = np.dot(hidden_t_prev, reset_gate_w.T) + reset_gate_b
        reset_gate = reset_gate + input_reset

        update_gate = np.dot(hidden_t_prev, update_gate_w.T) + update_gate_b
        update_gate = update_gate + input_update

        if linear_before_reset:
            with_linear = np.dot(
                hidden_t_prev, output_gate_w.T) + output_gate_b
            output_gate = sigmoid(reset_gate) * with_linear
        else:
            with_reset = hidden_t_prev * sigmoid(reset_gate)
            output_gate = np.dot(with_reset, output_gate_w.T) + output_gate_b
        output_gate = output_gate + input_output

        gates_out_t = np.concatenate(
            (reset_gate, update_gate, output_gate),
            axis=2,
        )
        print(reset_gate, update_gate, output_gate, gates_out_t, sep="\n")

        (hidden_t, ) = gru_unit(
            hidden_t_prev,
            gates_out_t,
            seq_lengths,
            t,
            drop_states=drop_states
        )
        hidden[t + 1] = hidden_t

    return (
        hidden[1:],
        hidden[-1].reshape(1, N, D),
    )
