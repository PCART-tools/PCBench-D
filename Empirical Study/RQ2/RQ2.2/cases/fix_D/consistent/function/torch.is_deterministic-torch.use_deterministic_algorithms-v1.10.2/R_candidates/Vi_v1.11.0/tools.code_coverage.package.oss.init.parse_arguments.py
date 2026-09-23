def parse_arguments(
    parser: argparse.ArgumentParser,
) -> Tuple[Option, Optional[List[str]], Optional[List[str]], Optional[bool]]:
    # parse args
    args = parser.parse_args()
    # get option
    options = get_options(args)
    return (options, args.interest_only, args.run_only, args.clean)
