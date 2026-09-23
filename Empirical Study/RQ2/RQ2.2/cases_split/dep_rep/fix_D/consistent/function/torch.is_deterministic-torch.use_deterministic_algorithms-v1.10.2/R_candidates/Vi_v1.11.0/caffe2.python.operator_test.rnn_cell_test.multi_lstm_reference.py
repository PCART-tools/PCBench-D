def multi_lstm_reference(input, hidden_input_list, cell_input_list,
                            i2h_w_list, i2h_b_list, gates_w_list, gates_b_list,
                            seq_lengths, forget_bias, drop_states=False):
    num_layers = len(hidden_input_list)
    assert len(cell_input_list) == num_layers
    assert len(i2h_w_list) == num_layers
    assert len(i2h_b_list) == num_layers
    assert len(gates_w_list) == num_layers
    assert len(gates_b_list) == num_layers

    for i in range(num_layers):
        layer_input = np.dot(input, i2h_w_list[i].T) + i2h_b_list[i]
        h_all, h_last, c_all, c_last = lstm_reference(
            layer_input,
            hidden_input_list[i],
            cell_input_list[i],
            gates_w_list[i],
            gates_b_list[i],
            seq_lengths,
            forget_bias,
            drop_states=drop_states,
        )
        input = h_all
    return h_all, h_last, c_all, c_last
