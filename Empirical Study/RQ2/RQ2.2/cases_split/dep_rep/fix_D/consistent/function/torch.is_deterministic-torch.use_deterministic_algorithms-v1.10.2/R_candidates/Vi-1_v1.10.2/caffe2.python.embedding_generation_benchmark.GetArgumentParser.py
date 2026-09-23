def GetArgumentParser():
    parser = argparse.ArgumentParser(
        description="Embedding generation benchmark."
    )

    parser.add_argument(
        "--embedding_size",
        type=int,
        default=512,
        help="Embedding size",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=16,
        help="The batch size."
    )
    parser.add_argument(
        "--data_size",
        type=int,
        default=10000,
        help="Number of sequences to generate"
    )
    parser.add_argument(
        "--seq_length",
        type=int,
        default=128,
        help="Max sequence length"
    )
    parser.add_argument(
        "--iters_to_report",
        type=int,
        default=20,
        help="Number of iterations to report progress"
    )
    parser.add_argument(
        "--implementation",
        type=str,
        default="sinusoid",
        help="'table' or 'sinusoid'",
    )
    return parser
