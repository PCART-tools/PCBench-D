def benchmark_concat(num_inputs, input_dim, axis, add_axis, iterations):
    input_names = [f"input{i}" for i in range(num_inputs)]
    for n in input_names:
        workspace.FeedBlob(n, np.random.randn(*input_dim).astype(np.float32))

    net = core.Net("benchmark_net")
    net.Concat(input_names, ["output", "split_info"], axis=axis, add_axis=add_axis)
    workspace.CreateNet(net)

    runtimes = workspace.BenchmarkNet(net.Name(), 1, iterations, True)
    print(f"{num_inputs * np.prod(input_dim) * 4 / runtimes[1] / 1e6} GB/s")
