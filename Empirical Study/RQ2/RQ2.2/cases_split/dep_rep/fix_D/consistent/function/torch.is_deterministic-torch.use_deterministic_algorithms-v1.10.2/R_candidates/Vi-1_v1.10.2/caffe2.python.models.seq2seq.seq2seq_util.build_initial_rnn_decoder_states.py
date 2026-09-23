def build_initial_rnn_decoder_states(
    model,
    encoder_units_per_layer,
    decoder_units_per_layer,
    final_encoder_hidden_states,
    final_encoder_cell_states,
    use_attention,
):
    num_encoder_layers = len(encoder_units_per_layer)
    num_decoder_layers = len(decoder_units_per_layer)
    if num_encoder_layers > num_decoder_layers:
        offset = num_encoder_layers - num_decoder_layers
    else:
        offset = 0

    initial_states = []
    for i, decoder_num_units in enumerate(decoder_units_per_layer):

        if (
            final_encoder_hidden_states and
            len(final_encoder_hidden_states) > (i + offset)
        ):
            final_encoder_hidden_state = final_encoder_hidden_states[i + offset]
        else:
            final_encoder_hidden_state = None

        if final_encoder_hidden_state is None:
            decoder_initial_hidden_state = model.param_init_net.ConstantFill(
                [],
                'decoder_initial_hidden_state_{}'.format(i),
                shape=[decoder_num_units],
                value=0.0,
            )
            model.params.append(decoder_initial_hidden_state)
        elif decoder_num_units != encoder_units_per_layer[i + offset]:
            decoder_initial_hidden_state = brew.fc(
                model,
                final_encoder_hidden_state,
                'decoder_initial_hidden_state_{}'.format(i),
                encoder_units_per_layer[i + offset],
                decoder_num_units,
                axis=2,
            )
        else:
            decoder_initial_hidden_state = final_encoder_hidden_state
        initial_states.append(decoder_initial_hidden_state)

        if (
            final_encoder_cell_states and
            len(final_encoder_cell_states) > (i + offset)
        ):
            final_encoder_cell_state = final_encoder_cell_states[i + offset]
        else:
            final_encoder_cell_state = None

        if final_encoder_cell_state is None:
            decoder_initial_cell_state = model.param_init_net.ConstantFill(
                [],
                'decoder_initial_cell_state_{}'.format(i),
                shape=[decoder_num_units],
                value=0.0,
            )
            model.params.append(decoder_initial_cell_state)
        elif decoder_num_units != encoder_units_per_layer[i + offset]:
            decoder_initial_cell_state = brew.fc(
                model,
                final_encoder_cell_state,
                'decoder_initial_cell_state_{}'.format(i),
                encoder_units_per_layer[i + offset],
                decoder_num_units,
                axis=2,
            )
        else:
            decoder_initial_cell_state = final_encoder_cell_state
        initial_states.append(decoder_initial_cell_state)

    if use_attention:
        initial_attention_weighted_encoder_context = (
            model.param_init_net.ConstantFill(
                [],
                'initial_attention_weighted_encoder_context',
                shape=[encoder_units_per_layer[-1]],
                value=0.0,
            )
        )
        model.params.append(initial_attention_weighted_encoder_context)
        initial_states.append(initial_attention_weighted_encoder_context)

    return initial_states
