def build_embedding_decoder(
    model,
    decoder_layer_configs,
    inputs,
    input_lengths,
    encoder_lengths,
    encoder_outputs,
    weighted_encoder_outputs,
    final_encoder_hidden_states,
    final_encoder_cell_states,
    encoder_units_per_layer,
    vocab_size,
    embeddings,
    embedding_size,
    attention_type,
    forward_only,
    num_gpus=0,
    scope=None,
):
    with core.NameScope(scope or ''):
        if num_gpus == 0:
            embedded_decoder_inputs = model.net.Gather(
                [embeddings, inputs],
                ['embedded_decoder_inputs'],
            )
        else:
            with core.DeviceScope(core.DeviceOption(caffe2_pb2.CPU)):
                embedded_decoder_inputs_cpu = model.net.Gather(
                    [embeddings, inputs],
                    ['embedded_decoder_inputs_cpu'],
                )
            embedded_decoder_inputs = model.CopyCPUToGPU(
                embedded_decoder_inputs_cpu,
                'embedded_decoder_inputs',
            )

    decoder_cells = []
    decoder_units_per_layer = []
    for i, layer_config in enumerate(decoder_layer_configs):
        num_units = layer_config['num_units']
        decoder_units_per_layer.append(num_units)

        if i == 0:
            input_size = embedding_size
        else:
            input_size = decoder_cells[-1].get_output_dim()

        cell = rnn_cell.LSTMCell(
            forward_only=forward_only,
            input_size=input_size,
            hidden_size=num_units,
            forget_bias=0.0,
            memory_optimization=False,
        )

        dropout_keep_prob = layer_config.get('dropout_keep_prob', None)
        if dropout_keep_prob is not None:
            dropout_ratio = 1.0 - layer_config.dropout_keep_prob
            cell = rnn_cell.DropoutCell(
                internal_cell=cell,
                dropout_ratio=dropout_ratio,
                forward_only=forward_only,
                is_test=False,
                name=get_layer_scope(scope, 'decoder_dropout', i),
            )

        decoder_cells.append(cell)

    states = build_initial_rnn_decoder_states(
        model=model,
        encoder_units_per_layer=encoder_units_per_layer,
        decoder_units_per_layer=decoder_units_per_layer,
        final_encoder_hidden_states=final_encoder_hidden_states,
        final_encoder_cell_states=final_encoder_cell_states,
        use_attention=(attention_type != 'none'),
    )
    attention_decoder = LSTMWithAttentionDecoder(
        encoder_outputs=encoder_outputs,
        encoder_output_dim=encoder_units_per_layer[-1],
        encoder_lengths=encoder_lengths,
        vocab_size=vocab_size,
        attention_type=attention_type,
        embedding_size=embedding_size,
        decoder_num_units=decoder_units_per_layer[-1],
        decoder_cells=decoder_cells,
        weighted_encoder_outputs=weighted_encoder_outputs,
        name=scope,
    )
    decoder_outputs, _ = attention_decoder.apply_over_sequence(
        model=model,
        inputs=embedded_decoder_inputs,
        seq_lengths=input_lengths,
        initial_states=states,
    )

    # we do softmax over the whole sequence
    # (max_length in the batch * batch_size) x decoder embedding size
    # -1 because we don't know max_length yet
    decoder_outputs_flattened, _ = model.net.Reshape(
        [decoder_outputs],
        [
            'decoder_outputs_flattened',
            'decoder_outputs_and_contexts_combination_old_shape',
        ],
        shape=[-1, attention_decoder.get_output_dim()],
    )

    decoder_outputs = decoder_outputs_flattened
    decoder_output_dim = attention_decoder.get_output_dim()

    return (decoder_outputs, decoder_output_dim)
