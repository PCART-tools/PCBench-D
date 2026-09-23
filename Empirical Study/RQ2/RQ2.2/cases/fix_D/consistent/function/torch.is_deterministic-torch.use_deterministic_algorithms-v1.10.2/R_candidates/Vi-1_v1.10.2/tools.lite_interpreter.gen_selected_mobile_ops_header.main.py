def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate selected_mobile_ops.h for selective build."
    )
    parser.add_argument(
        "-p", "--yaml_file_path", type=str, required=True, help="Path to the yaml"
        " file with a list of operators used by the model."
    )
    parser.add_argument(
        "-o", "--output_file_path", type=str, required=True, help="Path to destination"
        "folder where selected_mobile_ops.h will be written."
    )
    parsed_args = parser.parse_args()
    model_file_name = parsed_args.yaml_file_path

    print("Loading yaml file: ", model_file_name)
    loaded_model = {}
    with open(model_file_name, "rb") as model_file:
        loaded_model = yaml.load(model_file, Loader=Loader)


    root_operators_set = set(loaded_model)
    print("Writing header file selected_mobile_ops.h: ", parsed_args.output_file_path)
    write_selected_mobile_ops_with_all_dtypes(
        os.path.join(parsed_args.output_file_path, "selected_mobile_ops.h"),
        root_operators_set)
