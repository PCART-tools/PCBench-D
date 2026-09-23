def apply_soft_coverage_attention(
    model,
    encoder_output_dim,
    encoder_outputs_transposed,
    weighted_encoder_outputs,
    decoder_hidden_state_t,
    decoder_hidden_state_dim,
    scope,
    encoder_lengths,
    coverage_t_prev,
    coverage_weights,
):

    weighted_decoder_hidden_state = _apply_fc_weight_for_sum_match(
        model=model,
        input=decoder_hidden_state_t,
        dim_in=decoder_hidden_state_dim,
        dim_out=encoder_output_dim,
        scope=scope,
        name='weighted_decoder_hidden_state',
    )

    # [encoder_length, batch_size, encoder_output_dim]
    decoder_hidden_encoder_outputs_sum_tmp = model.net.Add(
        [weighted_encoder_outputs, weighted_decoder_hidden_state],
        s(scope, 'decoder_hidden_encoder_outputs_sum_tmp'),
        broadcast=1,
    )
    # [batch_size, encoder_length]
    coverage_t_prev_2d = model.net.Squeeze(
        coverage_t_prev,
        s(scope, 'coverage_t_prev_2d'),
        dims=[0],
    )
    # [encoder_length, batch_size]
    coverage_t_prev_transposed = brew.transpose(
        model,
        coverage_t_prev_2d,
        s(scope, 'coverage_t_prev_transposed'),
    )

    # [encoder_length, batch_size, encoder_output_dim]
    scaled_coverage_weights = model.net.Mul(
        [coverage_weights, coverage_t_prev_transposed],
        s(scope, 'scaled_coverage_weights'),
        broadcast=1,
        axis=0,
    )

    # [encoder_length, batch_size, encoder_output_dim]
    decoder_hidden_encoder_outputs_sum = model.net.Add(
        [decoder_hidden_encoder_outputs_sum_tmp, scaled_coverage_weights],
        s(scope, 'decoder_hidden_encoder_outputs_sum'),
    )

    # [batch_size, encoder_length, 1]
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

    # [batch_size, encoder_length]
    attention_weights_2d = model.net.Squeeze(
        attention_weights_3d,
        s(scope, 'attention_weights_2d'),
        dims=[2],
    )

    coverage_t = model.net.Add(
        [coverage_t_prev, attention_weights_2d],
        s(scope, 'coverage_t'),
        broadcast=1,
    )

    return (
        attention_weighted_encoder_context,
        attention_weights_3d,
        [decoder_hidden_encoder_outputs_sum],
        coverage_t,
    )
