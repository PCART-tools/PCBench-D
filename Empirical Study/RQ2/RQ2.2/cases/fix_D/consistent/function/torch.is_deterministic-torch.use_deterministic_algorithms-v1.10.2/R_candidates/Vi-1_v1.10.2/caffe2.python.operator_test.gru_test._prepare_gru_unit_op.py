def _prepare_gru_unit_op(gc, n, d, outputs_with_grads,
                         forward_only=False, drop_states=False,
                         sequence_lengths=False,
                         two_d_initial_states=None):
    print("Dims: (n,d) = ({},{})".format(n, d))

    def generate_input_state(n, d):
        if two_d_initial_states:
            return np.random.randn(n, d).astype(np.float32)
        else:
            return np.random.randn(1, n, d).astype(np.float32)

    model = ModelHelper(name='external')

    with scope.NameScope("test_name_scope"):
        if sequence_lengths:
            hidden_t_prev, gates_t, seq_lengths, timestep = \
                model.net.AddScopedExternalInputs(
                    "hidden_t_prev",
                    "gates_t",
                    'seq_lengths',
                    "timestep",
                )
        else:
            hidden_t_prev, gates_t, timestep = \
                model.net.AddScopedExternalInputs(
                    "hidden_t_prev",
                    "gates_t",
                    "timestep",
                )
        workspace.FeedBlob(
            hidden_t_prev,
            generate_input_state(n, d).astype(np.float32),
            device_option=gc
        )
        workspace.FeedBlob(
            gates_t,
            generate_input_state(n, 3 * d).astype(np.float32),
            device_option=gc
        )

        if sequence_lengths:
            inputs = [hidden_t_prev, gates_t, seq_lengths, timestep]
        else:
            inputs = [hidden_t_prev, gates_t, timestep]

        hidden_t = model.net.GRUUnit(
            inputs,
            ['hidden_t'],
            forget_bias=0.0,
            drop_states=drop_states,
            sequence_lengths=sequence_lengths,
        )
        model.net.AddExternalOutputs(hidden_t)
        workspace.RunNetOnce(model.param_init_net)

        if sequence_lengths:
            # 10 is used as a magic number to simulate some reasonable timestep
            # and generate some reasonable seq. lengths
            workspace.FeedBlob(
                seq_lengths,
                np.random.randint(1, 10, size=(n,)).astype(np.int32),
                device_option=gc
            )

        workspace.FeedBlob(
            timestep,
            np.random.randint(1, 10, size=(1,)).astype(np.int32),
            device_option=core.DeviceOption(caffe2_pb2.CPU),
        )
        print("Feed {}".format(timestep))

    return hidden_t, model.net
