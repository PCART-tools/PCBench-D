def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--op", default="add_op", dest="op", type=str)
    parser.add_argument("--benchmark_c2_net", default=False, dest="benchmark_c2_net", action="store_true")
    parser.add_argument("--use_throughput_benchmark", default=False, dest="use_throughput_benchmark", action="store_true")
    parser.add_argument("--debug", default=False, dest="debug", action="store_true")
    parser.add_argument("--save", default=False, dest="save", action="store_true")
    parser.add_argument("--eager_mode", default=False, dest="eager_mode", action="store_true")
    parser.add_argument("--num_warmup_iters", type=int, default=100)
    parser.add_argument("--num_iters", type=int, default=1000)
    args = parser.parse_args()

    if args.op not in SUPPORTED_OPS:
        print("Op {} is not supported: Supported ops are:{}".format(args.op, SUPPORTED_OPS))
        return
    assert not (args.benchmark_c2_net and args.use_throughput_benchmark), \
        "Benchmarking of C2 net via throughput benchmarking is not yet supported"

    num_warmup_iters = args.num_warmup_iters
    num_iters = args.num_iters
    config = BenchmarkConfig(num_warmup_iters, num_iters)
    graph_mode = True
    if args.eager_mode:
        graph_mode = False
    result = {}
    if args.op == "add_op":
        num_params = 2
        if args.benchmark_c2_net:
            module_config = ModuleConfig(None, 'Sum', num_params, None)
        else:
            module_config = ModuleConfig(add_tensors_loop, None, num_params, graph_mode)
        benchmark_simple_fn(args, config, module_config, SimpleAddModule, result)
    print_results(result)
