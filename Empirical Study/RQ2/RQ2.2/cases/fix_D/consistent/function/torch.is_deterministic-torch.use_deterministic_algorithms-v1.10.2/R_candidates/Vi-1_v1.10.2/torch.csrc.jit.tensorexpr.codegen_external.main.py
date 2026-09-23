def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate annotated_fn_args script')
    parser.add_argument('--native_functions',
                        help='path to native_functions.yaml',
                        default='../../../../aten/src/ATen/native/native_functions.yaml')
    parser.add_argument('--template_path',
                        help='path to external_functions_codegen_template.cpp',
                        default='../../../../tools/jit/templates/external_functions_codegen_template.cpp')
    args = parser.parse_args()
    gen_external(args.native_functions, args.template_path)
