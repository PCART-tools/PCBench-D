def create_model(args, queue, label_queue, input_shape):
    model = model_helper.ModelHelper(name="LSTM_bench")
    seq_lengths, target = \
        model.net.AddExternalInputs(
            'seq_lengths',
            'target',
        )

    input_blob = model.net.DequeueBlobs(queue, "input_data")
    labels = model.net.DequeueBlobs(label_queue, "label")

    init_blobs = []
    if args.implementation in ["own", "static", "static_dag"]:
        T = None
        if "static" in args.implementation:
            assert args.fixed_shape, \
                "Random input length is not static RNN compatible"
            T = args.seq_length
            print("Using static RNN of size {}".format(T))

        for i in range(args.num_layers):
            hidden_init, cell_init = model.net.AddExternalInputs(
                "hidden_init_{}".format(i),
                "cell_init_{}".format(i)
            )
            init_blobs.extend([hidden_init, cell_init])

        output, last_hidden, _, last_state = rnn_cell.LSTM(
            model=model,
            input_blob=input_blob,
            seq_lengths=seq_lengths,
            initial_states=init_blobs,
            dim_in=args.input_dim,
            dim_out=[args.hidden_dim] * args.num_layers,
            scope="lstm1",
            memory_optimization=args.memory_optimization,
            forward_only=args.forward_only,
            drop_states=True,
            return_last_layer_only=True,
            static_rnn_unroll_size=T,
        )

        if "dag" in args.implementation:
            print("Using DAG net type")
            model.net.Proto().type = 'dag'
            model.net.Proto().num_workers = 4

    elif args.implementation == "cudnn":
        # We need to feed a placeholder input so that RecurrentInitOp
        # can infer the dimensions.
        init_blobs = model.net.AddExternalInputs("hidden_init", "cell_init")
        model.param_init_net.ConstantFill([], input_blob, shape=input_shape)
        output, last_hidden, _ = rnn_cell.cudnn_LSTM(
            model=model,
            input_blob=input_blob,
            initial_states=init_blobs,
            dim_in=args.input_dim,
            dim_out=args.hidden_dim,
            scope="cudnnlstm",
            num_layers=args.num_layers,
        )

    else:
        assert False, "Unknown implementation"

    weights = model.net.UniformFill(labels, "weights")
    softmax, loss = model.net.SoftmaxWithLoss(
        [model.Flatten(output), labels, weights],
        ['softmax', 'loss'],
    )

    if not args.forward_only:
        model.AddGradientOperators([loss])

    # carry states over
    for init_blob in init_blobs:
        model.net.Copy(last_hidden, init_blob)

        sz = args.hidden_dim
        if args.implementation == "cudnn":
            sz *= args.num_layers
        workspace.FeedBlob(init_blob, np.zeros(
            [1, args.batch_size, sz], dtype=np.float32
        ))

    if args.rnn_executor:
        for op in model.net.Proto().op:
            if op.type.startswith('RecurrentNetwork'):
                recurrent.set_rnn_executor_config(
                    op,
                    num_threads=args.rnn_executor_num_threads,
                    max_cuda_streams=args.rnn_executor_max_cuda_streams,
                )
    return model, output
