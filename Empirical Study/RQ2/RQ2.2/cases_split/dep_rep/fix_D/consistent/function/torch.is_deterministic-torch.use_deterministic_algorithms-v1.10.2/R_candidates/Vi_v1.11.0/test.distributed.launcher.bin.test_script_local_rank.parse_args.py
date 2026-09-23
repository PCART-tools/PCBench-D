def parse_args():
    parser = argparse.ArgumentParser(description="test script")

    parser.add_argument(
        "--local_rank",
        type=int,
        required=True,
        help="The rank of the node for multi-node distributed " "training",
    )

    return parser.parse_args()
