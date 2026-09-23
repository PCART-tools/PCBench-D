def _calc_weighted_context(
    model,
    encoder_outputs_transposed,
    encoder_output_dim,
    attention_weights_3d,
    scope,
):
    # [batch_size, encoder_output_dim, 1]
    attention_weighted_encoder_context = brew.batch_mat_mul(
        model,
        [encoder_outputs_transposed, attention_weights_3d],
        s(scope, 'attention_weighted_encoder_context'),
    )
    # [batch_size, encoder_output_dim]
    attention_weighted_encoder_context, _ = model.net.Reshape(
        attention_weighted_encoder_context,
        [
            attention_weighted_encoder_context,
            s(scope, 'attention_weighted_encoder_context_old_shape'),
        ],
        shape=[1, -1, encoder_output_dim],
    )
    return attention_weighted_encoder_context
