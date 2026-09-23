def lstm_with_attention_reference(
    input,
    initial_hidden_state,
    initial_cell_state,
    initial_attention_weighted_encoder_context,
    gates_w,
    gates_b,
    decoder_input_lengths,
    encoder_outputs_transposed,
    weighted_prev_attention_context_w,
    weighted_prev_attention_context_b,
    weighted_decoder_hidden_state_t_w,
    weighted_decoder_hidden_state_t_b,
    weighted_encoder_outputs,
    coverage_weights,
    attention_v,
    attention_zeros,
    compute_attention_logits,
):
    encoder_outputs = np.transpose(encoder_outputs_transposed, axes=[2, 0, 1])
    encoder_outputs_for_dot_product = np.transpose(
        encoder_outputs_transposed,
        [0, 2, 1],
    )
    decoder_input_length = input.shape[0]
    batch_size = input.shape[1]
    decoder_input_dim = input.shape[2]
    decoder_state_dim = initial_hidden_state.shape[2]
    encoder_output_dim = encoder_outputs.shape[2]
    hidden = np.zeros(
        shape=(decoder_input_length + 1, batch_size, decoder_state_dim))
    cell = np.zeros(
        shape=(decoder_input_length + 1, batch_size, decoder_state_dim))
    attention_weighted_encoder_context = np.zeros(
        shape=(decoder_input_length + 1, batch_size, encoder_output_dim))
    cell[0, :, :] = initial_cell_state
    hidden[0, :, :] = initial_hidden_state
    attention_weighted_encoder_context[0, :, :] = (
        initial_attention_weighted_encoder_context
    )
    encoder_length = encoder_outputs.shape[0]
    coverage = np.zeros(
        shape=(decoder_input_length + 1, batch_size, encoder_length))
    for t in range(decoder_input_length):
        input_t = input[t].reshape(1, batch_size, decoder_input_dim)
        hidden_t_prev = hidden[t].reshape(1, batch_size, decoder_state_dim)
        cell_t_prev = cell[t].reshape(1, batch_size, decoder_state_dim)
        attention_weighted_encoder_context_t_prev = (
            attention_weighted_encoder_context[t].reshape(
                1, batch_size, encoder_output_dim)
        )
        gates_input = np.concatenate(
            (hidden_t_prev, attention_weighted_encoder_context_t_prev),
            axis=2,
        )
        gates = np.dot(gates_input, gates_w.T) + gates_b
        gates = gates + input_t
        hidden_t, cell_t = lstm_unit(hidden_t_prev, cell_t_prev, gates,
                                     decoder_input_lengths, t)
        hidden[t + 1] = hidden_t
        cell[t + 1] = cell_t

        coverage_prev = coverage[t].reshape(1, batch_size, encoder_length)

        attention_logits_t = compute_attention_logits(
            hidden_t,
            weighted_decoder_hidden_state_t_w,
            weighted_decoder_hidden_state_t_b,
            attention_weighted_encoder_context_t_prev,
            weighted_prev_attention_context_w,
            weighted_prev_attention_context_b,
            attention_v,
            weighted_encoder_outputs,
            encoder_outputs_for_dot_product,
            coverage_prev,
            coverage_weights,
        )

        attention_logits_t_exp = np.exp(attention_logits_t)
        attention_weights_t = (
            attention_logits_t_exp /
            np.sum(attention_logits_t_exp, axis=0).reshape([1, -1])
        )
        coverage[t + 1, :, :] = coverage[t, :, :] + attention_weights_t.T
        attention_weighted_encoder_context[t + 1] = np.sum(
            (
                encoder_outputs *
                attention_weights_t.reshape([-1, batch_size, 1])
            ),
            axis=0,
        )
    return (
        hidden[1:],
        hidden[-1].reshape(1, batch_size, decoder_state_dim),
        cell[1:],
        cell[-1].reshape(1, batch_size, decoder_state_dim),
        attention_weighted_encoder_context[1:],
        attention_weighted_encoder_context[-1].reshape(
            1,
            batch_size,
            encoder_output_dim,
        )
    )
