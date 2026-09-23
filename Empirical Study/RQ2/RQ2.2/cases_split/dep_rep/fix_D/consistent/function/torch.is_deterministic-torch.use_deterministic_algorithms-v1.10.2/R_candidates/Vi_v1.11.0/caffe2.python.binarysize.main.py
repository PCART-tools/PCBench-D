def main(argv):
    if not sys.platform.startswith('linux'):
        raise RuntimeError('Currently this tool only supports Linux.')
    parser = argparse.ArgumentParser(
        description="Tool to inspect binary size.")
    parser.add_argument(
        '--max_depth', type=int, default=10,
        help='The maximum depth to print the symbol tree.')
    parser.add_argument(
        '--min_size', type=int, default=1024,
        help='The mininum symbol size to print.')
    parser.add_argument(
        '--nm_command', type=str, default='nm',
        help='The path to the nm command that the tool needs.')
    parser.add_argument(
        '--color', action='store_true',
        help='If set, use ascii color for output.')
    parser.add_argument(
        '--target', type=str,
        help='The binary target to inspect.')
    args = parser.parse_args(argv)
    if not args.target:
        raise RuntimeError('You must specify a target to inspect.')
    symbol_trie = GetSymbolTrie(
        args.target, args.nm_command, args.max_depth)
    PrintTrie(symbol_trie, '', args.max_depth, args.min_size, args.color)
