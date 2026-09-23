def _calc_attention_logits_from_sum_match(
    model,
    decoder_hidden_encoder_outputs_sum,
    encoder_output_dim,
    scope,
):
    # [encoder_length, batch_size, encoder_output_dim]
    decoder_hidden_encoder_outputs_sum = model.net.Tanh(
        decoder_hidden_encoder_outputs_sum,
        decoder_hidden_encoder_outputs_sum,
    )

    # [encoder_length, batch_size, 1]
    attention_logits = brew.fc(
        model,
        decoder_hidden_encoder_outputs_sum,
        s(scope, 'attention_logits'),
        dim_in=encoder_output_dim,
        dim_out=1,
        axis=2,
        freeze_bias=True,
    )

    # [batch_size, encoder_length, 1]
    attention_logits_transposed = brew.transpose(
        model,
        attention_logits,
        s(scope, 'attention_logits_transposed'),
        axes=[1, 0, 2],
    )
    return attention_logits_transposed
