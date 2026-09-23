def compute_dot_attention_logits(
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
    hidden_t_for_dot_product = np.transpose(hidden_t, axes=[1, 2, 0])
    if (
        weighted_decoder_hidden_state_t_w is not None and
        weighted_decoder_hidden_state_t_b is not None
    ):
        hidden_t_for_dot_product = np.matmul(
            weighted_decoder_hidden_state_t_w,
            hidden_t_for_dot_product,
        ) + np.expand_dims(weighted_decoder_hidden_state_t_b, axis=1)
    attention_logits_t = np.sum(
        np.matmul(
            encoder_outputs_for_dot_product,
            hidden_t_for_dot_product,
        ),
        axis=2,
    )
    return np.transpose(attention_logits_t)
