def GetArgumentParser():
    parser = argparse.ArgumentParser(description="LSTM benchmark.")

    parser.add_argument(
        "--hidden_dim",
        type=int,
        default=800,
        help="Hidden dimension",
    )
    parser.add_argument(
        "--input_dim",
        type=int,
        default=40,
        help="Input dimension",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=128,
        help="The batch size."
    )
    parser.add_argument(
        "--seq_length",
        type=int,
        default=20,
        help="Max sequence length"
    )
    parser.add_argument(
        "--data_size",
        type=int,
        default=1000000,
        help="Number of data points to generate"
    )
    parser.add_argument(
        "--iters_to_report",
        type=int,
        default=20,
        help="Number of iteration to report progress"
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Run all on GPU",
    )
    parser.add_argument(
        "--implementation",
        type=str,
        default="own",
        help="'cudnn', 'own', 'static' or 'static_dag'",
    )
    parser.add_argument(
        "--fixed_shape",
        action="store_true",
        help=("Whether to randomize shape of input batches. "
              "Static RNN requires fixed shape"),
    )
    parser.add_argument(
        "--memory_optimization",
        action="store_true",
        help="Whether to use memory optimized LSTM or not",
    )
    parser.add_argument(
        "--forward_only",
        action="store_true",
        help="Whether to run only forward pass"
    )
    parser.add_argument(
        "--num_layers",
        type=int,
        default=1,
        help="Number of LSTM layers. All output dimensions are going to be"
             "of hidden_dim size",
    )
    parser.add_argument(
        "--rnn_executor",
        action="store_true",
        help="Whether to use RNN executor"
    )
    parser.add_argument(
        "--rnn_executor_num_threads",
        type=int,
        default=None,
        help="Number of threads used by CPU RNN Executor"
    )
    parser.add_argument(
        "--rnn_executor_max_cuda_streams",
        type=int,
        default=None,
        help="Maximum number of CUDA streams used by RNN executor on GPU"
    )
    return parser
