def main(args):
    # User defined keyword arguments
    kwargs = {"order": "NCHW", "use_cudnn": False}
    kwargs.update(dict(args.kwargs))

    model = ModelHelper(name=args.benchmark_name)

    op_type = args.operator  # assumes a brew type op name
    input_name = args.input_name
    output_name = args.output_name

    iters = int(args.instances)
    for i in range(iters):
        input_blob_name = input_name + (str(i) if i > 0 and args.chain else '')
        output_blob_name = output_name + str(i + 1)
        add_op = getattr(brew, op_type)
        add_op(model, input_blob_name, output_blob_name, **kwargs)
        if args.chain:
            input_name, output_name = output_name, input_name

    workspace.RunNetOnce(model.param_init_net)

    init_net, predict_net = mobile_exporter.Export(
        workspace, model.net, model.params
    )

    if args.debug:
        print("init_net:")
        for op in init_net.op:
            print(" ", op.type, op.input, "-->", op.output)
        print("predict_net:")
        for op in predict_net.op:
            print(" ", op.type, op.input, "-->", op.output)

    with open(args.predict_net, 'wb') as f:
        f.write(predict_net.SerializeToString())
    with open(args.init_net, 'wb') as f:
        f.write(init_net.SerializeToString())
