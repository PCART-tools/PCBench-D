def reproString(current_seed, args):
    repro_str = "python {0}".format(__file__)
    if args.cuda_fuser:
        repro_str += " --cuda_fuser"
    if args.legacy_fuser:
        repro_str += " --legacy_fuser"
    if args.profiling_executor:
        repro_str += " --profiling_executor"
    if args.fp16:
        repro_str += " --fp16"
    if args.cpu:
        repro_str += " --cpu"
    repro_str += " --max_num_tensor {0} --max_tensor_dim {1} --max_tensor_size {2}"\
        " --depth_factor {3} --seed {4} --repro_run".format(
            args.max_num_tensor, args.max_tensor_dim, args.max_tensor_size,
            args.depth_factor, current_seed)
    return repro_str
