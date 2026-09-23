def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate annotated_fn_args script')
    parser.add_argument('native_functions', metavar='NATIVE',
                        help='path to native_functions.yaml')
    parser.add_argument('out', metavar='OUT',
                        help='path to output directory')
    parser.add_argument('autograd', metavar='AUTOGRAD',
                        help='path to template directory')
    args = parser.parse_args()
    gen_annotated(args.native_functions, args.out, args.autograd)
