def Benchmark(model_gen, arg):
    model, input_size = model_gen(arg.order)
    model.Proto().type = arg.net_type
    model.Proto().num_workers = arg.num_workers

    # In order to be able to run everything without feeding more stuff, let's
    # add the data and label blobs to the parameter initialization net as well.

    if arg.order == "NCHW":
        input_shape = [arg.batch_size, 3, input_size, input_size]
    else:
        input_shape = [arg.batch_size, input_size, input_size, 3]
        if arg.model == "MLP":
            input_shape = [arg.batch_size, input_size]

    model.param_init_net.GaussianFill(
        [],
        "data",
        shape=input_shape,
        mean=0.0,
        std=1.0
    )
    model.param_init_net.UniformIntFill(
        [],
        "label",
        shape=[arg.batch_size, ],
        min=0,
        max=999
    )

    if arg.forward_only:
        print('{}: running forward only.'.format(arg.model))
    else:
        print('{}: running forward-backward.'.format(arg.model))
        model.AddGradientOperators(["loss"])
        AddParameterUpdate(model)

        if arg.order == 'NHWC':
            print(
                '==WARNING==\n'
                'NHWC order with CuDNN may not be supported yet, so I might\n'
                'exit suddenly.'
            )

    if not arg.cpu:
        model.param_init_net.RunAllOnGPU()
        model.net.RunAllOnGPU()

    if arg.dump_model:
        # Writes out the pbtxt for benchmarks on e.g. Android
        with open(
            "{0}_init_batch_{1}.pbtxt".format(arg.model, arg.batch_size), "w"
        ) as fid:
            fid.write(str(model.param_init_net.Proto()))
            with open("{0}.pbtxt".format(arg.model), "w") as fid:
                fid.write(str(model.net.Proto()))

    workspace.RunNetOnce(model.param_init_net)
    workspace.CreateNet(model.net)
    for i in range(arg.warmup_iterations):
        workspace.RunNet(model.net.Proto().name)

    plan = core.Plan("plan")
    plan.AddStep(core.ExecutionStep("run", model.net, arg.iterations))
    start = time.time()
    workspace.RunPlan(plan)
    print('Spent: {}'.format((time.time() - start) / arg.iterations))
    if arg.layer_wise_benchmark:
        print('Layer-wise benchmark.')
        workspace.BenchmarkNet(model.net.Proto().name, 1, arg.iterations, True)
