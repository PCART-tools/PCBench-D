def benchmark_mul_gradient(args):
    workspace.FeedBlob("dC", np.random.rand(args.m, args.n).astype(np.float32))
    workspace.FeedBlob("A", np.random.rand(args.m, args.n).astype(np.float32))
    workspace.FeedBlob("B", np.random.rand(args.n).astype(np.float32))

    net = core.Net("mynet")
    net.MulGradient(
        ["dC", "A", "B"],
        ["dC" if args.inplace else "dA", "dB"],
        broadcast=True,
        axis=1,
        allow_broadcast_fastpath=args.allow_broadcast_fastpath,
    )
    workspace.CreateNet(net)

    workspace.BenchmarkNet(net.Name(), 1, args.iteration, True)
