def cudnn_LSTM(model, input_blob, initial_states, dim_in, dim_out,
               scope, recurrent_params=None, input_params=None,
               num_layers=1, return_params=False):
    '''
    CuDNN version of LSTM for GPUs.
    input_blob          Blob containing the input. Will need to be available
                        when param_init_net is run, because the sequence lengths
                        and batch sizes will be inferred from the size of this
                        blob.
    initial_states      tuple of (hidden_init, cell_init) blobs
    dim_in              input dimensions
    dim_out             output/hidden dimension
    scope               namescope to apply
    recurrent_params    dict of blobs containing values for recurrent
                        gate weights, biases (if None, use random init values)
                        See GetLSTMParamNames() for format.
    input_params        dict of blobs containing values for input
                        gate weights, biases (if None, use random init values)
                        See GetLSTMParamNames() for format.
    num_layers          number of LSTM layers
    return_params       if True, returns (param_extract_net, param_mapping)
                        where param_extract_net is a net that when run, will
                        populate the blobs specified in param_mapping with the
                        current gate weights and biases (input/recurrent).
                        Useful for assigning the values back to non-cuDNN
                        LSTM.
    '''
    with core.NameScope(scope):
        weight_params = GetLSTMParamNames()['weights']
        bias_params = GetLSTMParamNames()['biases']

        input_weight_size = dim_out * dim_in
        upper_layer_input_weight_size = dim_out * dim_out
        recurrent_weight_size = dim_out * dim_out
        input_bias_size = dim_out
        recurrent_bias_size = dim_out

        def init(layer, pname, input_type):
            input_weight_size_for_layer = input_weight_size if layer == 0 else \
                upper_layer_input_weight_size
            if pname in weight_params:
                sz = input_weight_size_for_layer if input_type == 'input' \
                    else recurrent_weight_size
            elif pname in bias_params:
                sz = input_bias_size if input_type == 'input' \
                    else recurrent_bias_size
            else:
                assert False, "unknown parameter type {}".format(pname)
            return model.param_init_net.UniformFill(
                [],
                "lstm_init_{}_{}_{}".format(input_type, pname, layer),
                shape=[sz])

        # Multiply by 4 since we have 4 gates per LSTM unit
        first_layer_sz = input_weight_size + recurrent_weight_size + \
                         input_bias_size + recurrent_bias_size
        upper_layer_sz = upper_layer_input_weight_size + \
                         recurrent_weight_size + input_bias_size + \
                         recurrent_bias_size
        total_sz = 4 * (first_layer_sz + (num_layers - 1) * upper_layer_sz)

        weights = model.create_param(
            'lstm_weight',
            shape=[total_sz],
            initializer=Initializer('UniformFill'),
            tags=ParameterTags.WEIGHT,
        )

        lstm_args = {
            'hidden_size': dim_out,
            'rnn_mode': 'lstm',
            'bidirectional': 0,  # TODO
            'dropout': 1.0,  # TODO
            'input_mode': 'linear',  # TODO
            'num_layers': num_layers,
            'engine': 'CUDNN'
        }

        param_extract_net = core.Net("lstm_param_extractor")
        param_extract_net.AddExternalInputs([input_blob, weights])
        param_extract_mapping = {}

        # Populate the weights-blob from blobs containing parameters for
        # the individual components of the LSTM, such as forget/input gate
        # weights and bises. Also, create a special param_extract_net that
        # can be used to grab those individual params from the black-box
        # weights blob. These results can be then fed to InitFromLSTMParams()
        for input_type in ['input', 'recurrent']:
            param_extract_mapping[input_type] = {}
            p = recurrent_params if input_type == 'recurrent' else input_params
            if p is None:
                p = {}
            for pname in weight_params + bias_params:
                for j in range(0, num_layers):
                    values = p[pname] if pname in p else init(j, pname, input_type)
                    model.param_init_net.RecurrentParamSet(
                        [input_blob, weights, values],
                        weights,
                        layer=j,
                        input_type=input_type,
                        param_type=pname,
                        **lstm_args
                    )
                    if pname not in param_extract_mapping[input_type]:
                        param_extract_mapping[input_type][pname] = {}
                    b = param_extract_net.RecurrentParamGet(
                        [input_blob, weights],
                        ["lstm_{}_{}_{}".format(input_type, pname, j)],
                        layer=j,
                        input_type=input_type,
                        param_type=pname,
                        **lstm_args
                    )
                    param_extract_mapping[input_type][pname][j] = b

        (hidden_input_blob, cell_input_blob) = initial_states
        output, hidden_output, cell_output, rnn_scratch, dropout_states = \
            model.net.Recurrent(
                [input_blob, hidden_input_blob, cell_input_blob, weights],
                ["lstm_output", "lstm_hidden_output", "lstm_cell_output",
                 "lstm_rnn_scratch", "lstm_dropout_states"],
                seed=random.randint(0, 100000),  # TODO: dropout seed
                **lstm_args
            )
        model.net.AddExternalOutputs(
            hidden_output, cell_output, rnn_scratch, dropout_states)

    if return_params:
        param_extract = param_extract_net, param_extract_mapping
        return output, hidden_output, cell_output, param_extract
    else:
        return output, hidden_output, cell_output
