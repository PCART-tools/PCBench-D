def apply_dot_attention(
    model,
    encoder_output_dim,
    # [batch_size, encoder_output_dim, encoder_length]
    encoder_outputs_transposed,
    # [1, batch_size, decoder_state_dim]
    decoder_hidden_state_t,
    decoder_hidden_state_dim,
    scope,
    encoder_lengths=None,
):
    if decoder_hidden_state_dim != encoder_output_dim:
        weighted_decoder_hidden_state = brew.fc(
            model,
            decoder_hidden_state_t,
            s(scope, 'weighted_decoder_hidden_state'),
            dim_in=decoder_hidden_state_dim,
            dim_out=encoder_output_dim,
            axis=2,
        )
    else:
        weighted_decoder_hidden_state = decoder_hidden_state_t

    # [batch_size, decoder_state_dim]
    squeezed_weighted_decoder_hidden_state = model.net.Squeeze(
        weighted_decoder_hidden_state,
        s(scope, 'squeezed_weighted_decoder_hidden_state'),
        dims=[0],
    )

    # [batch_size, decoder_state_dim, 1]
    expanddims_squeezed_weighted_decoder_hidden_state = model.net.ExpandDims(
        squeezed_weighted_decoder_hidden_state,
        squeezed_weighted_decoder_hidden_state,
        dims=[2],
    )

    # [batch_size, encoder_output_dim, 1]
    attention_logits_transposed = model.net.BatchMatMul(
        [
            encoder_outputs_transposed,
            expanddims_squeezed_weighted_decoder_hidden_state,
        ],
        s(scope, 'attention_logits'),
        trans_a=1,
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
    return attention_weighted_encoder_context, attention_weights_3d, []
