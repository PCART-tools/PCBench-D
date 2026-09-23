def parse_args():
    parser = argparse.ArgumentParser(description="test script")

    parser.add_argument(
        "--init_method",
        type=str,
        required=True,
        help="init_method to pass to `dist.init_process_group()` (e.g. env://)",
    )
    parser.add_argument(
        "--world_size",
        type=int,
        default=os.getenv("WORLD_SIZE", -1),
        help="world_size to pass to `dist.init_process_group()`",
    )
    parser.add_argument(
        "--rank",
        type=int,
        default=os.getenv("RANK", -1),
        help="rank to pass to `dist.init_process_group()`",
    )

    return parser.parse_args()
