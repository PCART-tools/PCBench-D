def build_embedding_encoder(
    model,
    encoder_params,
    num_decoder_layers,
    inputs,
    input_lengths,
    vocab_size,
    embeddings,
    embedding_size,
    use_attention,
    num_gpus=0,
    forward_only=False,
    scope=None,
):
    with core.NameScope(scope or ''):
        if num_gpus == 0:
            embedded_encoder_inputs = model.net.Gather(
                [embeddings, inputs],
                ['embedded_encoder_inputs'],
            )
        else:
            with core.DeviceScope(core.DeviceOption(caffe2_pb2.CPU)):
                embedded_encoder_inputs_cpu = model.net.Gather(
                    [embeddings, inputs],
                    ['embedded_encoder_inputs_cpu'],
                )
            embedded_encoder_inputs = model.CopyCPUToGPU(
                embedded_encoder_inputs_cpu,
                'embedded_encoder_inputs',
            )

    layer_inputs = embedded_encoder_inputs
    layer_input_size = embedding_size
    encoder_units_per_layer = []
    final_encoder_hidden_states = []
    final_encoder_cell_states = []

    num_encoder_layers = len(encoder_params['encoder_layer_configs'])
    use_bidirectional_encoder = encoder_params.get(
        'use_bidirectional_encoder',
        False,
    )

    for i, layer_config in enumerate(encoder_params['encoder_layer_configs']):

        if use_bidirectional_encoder and i == 0:
            layer_func = rnn_bidirectional_layer
            output_dims = 2 * layer_config['num_units']
        else:
            layer_func = rnn_unidirectional_layer
            output_dims = layer_config['num_units']
        encoder_units_per_layer.append(output_dims)

        is_final_layer = (i == num_encoder_layers - 1)

        dropout_keep_prob = layer_config.get(
            'dropout_keep_prob',
            None,
        )

        return_final_state = i >= (num_encoder_layers - num_decoder_layers)
        (
            layer_outputs,
            final_layer_hidden_state,
            final_layer_cell_state,
        ) = layer_func(
            model=model,
            inputs=layer_inputs,
            input_lengths=input_lengths,
            input_size=layer_input_size,
            num_units=layer_config['num_units'],
            dropout_keep_prob=dropout_keep_prob,
            forward_only=forward_only,
            return_sequence_output=(not is_final_layer) or use_attention,
            return_final_state=return_final_state,
            scope=get_layer_scope(scope, 'encoder', i),
        )

        if not is_final_layer:
            layer_inputs = layer_outputs
            layer_input_size = output_dims
        final_encoder_hidden_states.append(final_layer_hidden_state)
        final_encoder_cell_states.append(final_layer_cell_state)

    encoder_outputs = layer_outputs
    weighted_encoder_outputs = None

    return (
        encoder_outputs,
        weighted_encoder_outputs,
        final_encoder_hidden_states,
        final_encoder_cell_states,
        encoder_units_per_layer,
    )
