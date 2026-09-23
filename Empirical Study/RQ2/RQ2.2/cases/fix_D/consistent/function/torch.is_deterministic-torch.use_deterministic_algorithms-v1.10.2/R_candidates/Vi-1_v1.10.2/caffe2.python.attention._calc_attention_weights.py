def _calc_attention_weights(
    model,
    attention_logits_transposed,
    scope,
    encoder_lengths=None,
):
    if encoder_lengths is not None:
        attention_logits_transposed = model.net.SequenceMask(
            [attention_logits_transposed, encoder_lengths],
            ['masked_attention_logits'],
            mode='sequence',
        )

    # [batch_size, encoder_length, 1]
    attention_weights_3d = brew.softmax(
        model,
        attention_logits_transposed,
        s(scope, 'attention_weights_3d'),
        engine='CUDNN',
        axis=1,
    )
    return attention_weights_3d
