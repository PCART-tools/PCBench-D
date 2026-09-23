def apply_recurrent_attention(
    model,
    encoder_output_dim,
    encoder_outputs_transposed,
    weighted_encoder_outputs,
    decoder_hidden_state_t,
    decoder_hidden_state_dim,
    attention_weighted_encoder_context_t_prev,
    scope,
    encoder_lengths=None,
):
    weighted_prev_attention_context = _apply_fc_weight_for_sum_match(
        model=model,
        input=attention_weighted_encoder_context_t_prev,
        dim_in=encoder_output_dim,
        dim_out=encoder_output_dim,
        scope=scope,
        name='weighted_prev_attention_context',
    )

    weighted_decoder_hidden_state = _apply_fc_weight_for_sum_match(
        model=model,
        input=decoder_hidden_state_t,
        dim_in=decoder_hidden_state_dim,
        dim_out=encoder_output_dim,
        scope=scope,
        name='weighted_decoder_hidden_state',
    )
    # [1, batch_size, encoder_output_dim]
    decoder_hidden_encoder_outputs_sum_tmp = model.net.Add(
        [
            weighted_prev_attention_context,
            weighted_decoder_hidden_state,
        ],
        s(scope, 'decoder_hidden_encoder_outputs_sum_tmp'),
    )
    # [encoder_length, batch_size, encoder_output_dim]
    decoder_hidden_encoder_outputs_sum = model.net.Add(
        [
            weighted_encoder_outputs,
            decoder_hidden_encoder_outputs_sum_tmp,
        ],
        s(scope, 'decoder_hidden_encoder_outputs_sum'),
        broadcast=1,
    )
    attention_logits_transposed = _calc_attention_logits_from_sum_match(
        model=model,
        decoder_hidden_encoder_outputs_sum=decoder_hidden_encoder_outputs_sum,
        encoder_output_dim=encoder_output_dim,
        scope=scope,
    )

    # [batch_size, encoder_length, 1]
    attention_weights_3d = _calc_attention_weights(
        model=model,
        attention_logits_transposed=attention_logits_transposed,
        scope=scope,
        encoder_lengths=encoder_lengths,
    )

    # [batch_size, encoder_output_dim, 1]
    attention_weighted_encoder_context = _calc_weighted_context(
        model=model,
        encoder_outputs_transposed=encoder_outputs_transposed,
        encoder_output_dim=encoder_output_dim,
        attention_weights_3d=attention_weights_3d,
        scope=scope,
    )
    return attention_weighted_encoder_context, attention_weights_3d, [
        decoder_hidden_encoder_outputs_sum,
    ]
