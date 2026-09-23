def benchmark_simple_fn(args, config, module_config, module_type, result):
    """ Benchmarks a PyTorch traceable function specified in the config.
    Instantiates a wrapper object that wraps the object of module_type and runs the forward
    method using benchmark_module.
    Args:
        config:         contains number of warmup and benchmark iterations.
        module_config:  module_config which contains op, number of parameters that op takes
                    and whether graph mode is enabled or not.
        module_type:    Type of the module to be wrapped. e.g. SimpleAddModule for add op.
        result:         dictionary instance to be populated with the benchmark result (latency per iter).
    """
    benchmark_c2_net = args.benchmark_c2_net
    print("Benchmarking {}".format(module_type.__name__))
    if benchmark_c2_net:
        op_name = module_config.c2_op
        num_inputs = module_config.num_params
        module = C2SimpleNet(op_name, num_inputs=num_inputs, debug=args.debug)
        latency_per_iter_ms = benchmark_module(config, module)
        result[op_name] = latency_per_iter_ms
    else:
        f_name = module_config.pt_fn.__name__ + ":Num Operands=" + str(module_config.num_params)
        graph_mode_str = "Graph mode" + ":" + str(module_config.graph_mode)
        result_key = ','.join((f_name, graph_mode_str))
        module = WrapperModule(module_type, module_config, args.debug, args.save)
        latency_per_iter_ms = benchmark_module(config, module, args.use_throughput_benchmark)
        result[result_key] = latency_per_iter_ms
