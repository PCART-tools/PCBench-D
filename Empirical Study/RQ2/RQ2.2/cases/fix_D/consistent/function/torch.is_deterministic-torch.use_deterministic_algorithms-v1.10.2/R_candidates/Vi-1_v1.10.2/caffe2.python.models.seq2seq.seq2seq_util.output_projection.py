def output_projection(
    model,
    decoder_outputs,
    decoder_output_size,
    target_vocab_size,
    decoder_softmax_size,
):
    if decoder_softmax_size is not None:
        decoder_outputs = brew.fc(
            model,
            decoder_outputs,
            'decoder_outputs_scaled',
            dim_in=decoder_output_size,
            dim_out=decoder_softmax_size,
        )
        decoder_output_size = decoder_softmax_size

    output_projection_w = model.param_init_net.XavierFill(
        [],
        'output_projection_w',
        shape=[target_vocab_size, decoder_output_size],
    )

    output_projection_b = model.param_init_net.XavierFill(
        [],
        'output_projection_b',
        shape=[target_vocab_size],
    )
    model.params.extend([
        output_projection_w,
        output_projection_b,
    ])
    output_logits = model.net.FC(
        [
            decoder_outputs,
            output_projection_w,
            output_projection_b,
        ],
        ['output_logits'],
    )
    return output_logits
