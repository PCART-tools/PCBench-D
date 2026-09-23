def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate type stubs for PyTorch')
    parser.add_argument('--native-functions-path', metavar='NATIVE',
                        default='aten/src/ATen/native/native_functions.yaml',
                        help='path to native_functions.yaml')
    parser.add_argument('--deprecated-functions-path', metavar='DEPRECATED',
                        default='tools/autograd/deprecated.yaml',
                        help='path to deprecated.yaml')
    parser.add_argument('--out', metavar='OUT',
                        default='.',
                        help='path to output directory')
    args = parser.parse_args()
    fm = FileManager(install_dir=args.out, template_dir='.', dry_run=False)
    gen_pyi(args.native_functions_path, args.deprecated_functions_path, fm)
