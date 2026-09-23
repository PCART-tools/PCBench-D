def main() -> None:
    parser = argparse.ArgumentParser(description='Autogenerate code')
    parser.add_argument('--declarations-path')
    parser.add_argument('--native-functions-path')
    parser.add_argument('--nn-path')
    parser.add_argument('--ninja-global')
    parser.add_argument('--install_dir')
    parser.add_argument(
        '--subset',
        help='Subset of source files to generate. Can be "libtorch" or "pybindings". Generates both when omitted.'
    )
    parser.add_argument(
        '--disable-autograd',
        default=False,
        action='store_true',
        help='It can skip generating autograd related code when the flag is set',
    )
    parser.add_argument(
        '--selected-op-list-path',
        help='Path to the YAML file that contains the list of operators to include for custom build.',
    )
    parser.add_argument(
        '--operators_yaml_path',
        help='Path to the model YAML file that contains the list of operators to include for custom build.',
    )
    parser.add_argument(
        '--force_schema_registration',
        action='store_true',
        help='force it to generate schema-only registrations for ops that are not'
        'listed on --selected-op-list'
    )
    options = parser.parse_args()

    generate_code(
        options.ninja_global,
        options.declarations_path,
        options.nn_path,
        options.native_functions_path,
        options.install_dir,
        options.subset,
        options.disable_autograd,
        options.force_schema_registration,
        # options.selected_op_list
        operator_selector=get_selector(options.selected_op_list_path, options.operators_yaml_path),
    )
