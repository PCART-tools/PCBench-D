def compute_regular_attention_logits(
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
):
    weighted_hidden_t = np.dot(
        hidden_t,
        weighted_decoder_hidden_state_t_w.T,
    ) + weighted_decoder_hidden_state_t_b
    attention_v = attention_v.reshape([-1])
    return np.sum(
        attention_v * np.tanh(weighted_encoder_outputs + weighted_hidden_t),
        axis=2,
    )
