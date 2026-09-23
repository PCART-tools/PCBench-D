def GetArgumentParser():
    parser = argparse.ArgumentParser(description="Caffe2 benchmark.")
    parser.add_argument(
        "--batch_size",
        type=int,
        default=128,
        help="The batch size."
    )
    parser.add_argument("--model", type=str, help="The model to benchmark.")
    parser.add_argument(
        "--order",
        type=str,
        default="NCHW",
        help="The order to evaluate."
    )
    parser.add_argument(
        "--cudnn_ws",
        type=int,
        default=-1,
        help="The cudnn workspace size."
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Number of iterations to run the network."
    )
    parser.add_argument(
        "--warmup_iterations",
        type=int,
        default=10,
        help="Number of warm-up iterations before benchmarking."
    )
    parser.add_argument(
        "--forward_only",
        action='store_true',
        help="If set, only run the forward pass."
    )
    parser.add_argument(
        "--layer_wise_benchmark",
        action='store_true',
        help="If True, run the layer-wise benchmark as well."
    )
    parser.add_argument(
        "--cpu",
        action='store_true',
        help="If True, run testing on CPU instead of GPU."
    )
    parser.add_argument(
        "--dump_model",
        action='store_true',
        help="If True, dump the model prototxts to disk."
    )
    parser.add_argument("--net_type", type=str, default="dag")
    parser.add_argument("--num_workers", type=int, default=2)
    return parser
