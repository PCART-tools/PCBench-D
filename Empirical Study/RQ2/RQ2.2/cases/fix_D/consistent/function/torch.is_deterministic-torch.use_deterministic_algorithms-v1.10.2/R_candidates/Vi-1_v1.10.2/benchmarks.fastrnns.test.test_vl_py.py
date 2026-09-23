def test_vl_py(**test_args):
    # XXX: This compares vl_py with vl_lstm.
    # It's done this way because those two don't give the same outputs so
    # the result isn't an apples-to-apples comparison right now.
    control_creator = varlen_pytorch_lstm_creator
    name, experim_creator, context = get_nn_runners('vl_py')[0]
    with context():
        print('testing {}...'.format(name))
        creator_keys = [
            'seqLength', 'numLayers', 'inputSize',
            'hiddenSize', 'miniBatch', 'device', 'seed'
        ]
        creator_args = {key: test_args[key] for key in creator_keys}

        print("Setting up...")
        control = control_creator(**creator_args)
        experim = experim_creator(**creator_args)

        # Precondition
        assertEqual(experim.inputs, control.inputs[:2])
        assertEqual(experim.params, control.params)

        print("Checking outputs...")
        control_out, control_hiddens = control.forward(*control.inputs)
        control_hx, control_cx = control_hiddens
        experim_out, experim_hiddens = experim.forward(*experim.inputs)
        experim_hx, experim_cx = experim_hiddens

        experim_padded = nn.utils.rnn.pad_sequence(experim_out).squeeze(-2)
        assertEqual(experim_padded, control_out)
        assertEqual(torch.cat(experim_hx, dim=1), control_hx)
        assertEqual(torch.cat(experim_cx, dim=1), control_cx)

        print("Checking grads...")
        assert control.backward_setup is not None
        assert experim.backward_setup is not None
        assert control.backward is not None
        assert experim.backward is not None
        control_backward_inputs = control.backward_setup(
            (control_out, control_hiddens), test_args['seed'])
        experim_backward_inputs = experim.backward_setup(
            (experim_out, experim_hiddens), test_args['seed'])

        control.backward(*control_backward_inputs)
        experim.backward(*experim_backward_inputs)

        control_grads = [p.grad for p in control.params]
        experim_grads = [p.grad for p in experim.params]
        assertEqual(experim_grads, control_grads)

        if test_args['verbose']:
            print(experim.forward.graph_for(*experim.inputs))
        print('')
