def lstm_with_dot_attention_reference_different_dim(
    input,
    initial_hidden_state,
    initial_cell_state,
    initial_attention_weighted_encoder_context,
    gates_w,
    gates_b,
    decoder_input_lengths,
    weighted_decoder_hidden_state_t_w,
    weighted_decoder_hidden_state_t_b,
    encoder_outputs_transposed,
):
    return lstm_with_dot_attention_reference(
        input=input,
        initial_hidden_state=initial_hidden_state,
        initial_cell_state=initial_cell_state,
        initial_attention_weighted_encoder_context=(
            initial_attention_weighted_encoder_context
        ),
        gates_w=gates_w,
        gates_b=gates_b,
        decoder_input_lengths=decoder_input_lengths,
        encoder_outputs_transposed=encoder_outputs_transposed,
        weighted_decoder_hidden_state_t_w=weighted_decoder_hidden_state_t_w,
        weighted_decoder_hidden_state_t_b=weighted_decoder_hidden_state_t_b,
    )
