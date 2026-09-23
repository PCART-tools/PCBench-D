def main():
    parser = argparse.ArgumentParser(description='Tool to check namespace content changes')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prev-version', action='store_true')
    group.add_argument('--new-version', action='store_true')
    group.add_argument('--compare', action='store_true')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--submod', default='', help='part of the submodule to check')
    group.add_argument('--all-submod', action='store_true', help='collects data for all main submodules')

    parser.add_argument('--show-all', action='store_true', help='show all the diff, not just public APIs')


    args = parser.parse_args()

    if args.all_submod:
        submods = all_submod_list
    else:
        submods = [args.submod]

    for mod in submods:
        run(args, mod)
