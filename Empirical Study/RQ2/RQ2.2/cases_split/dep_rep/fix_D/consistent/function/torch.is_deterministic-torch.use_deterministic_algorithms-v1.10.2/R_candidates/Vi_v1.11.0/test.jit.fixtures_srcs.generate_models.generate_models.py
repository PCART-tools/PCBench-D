def generate_models(model_directory_path: Path):
    all_models = get_all_models(model_directory_path)
    for a_module, expect_operator in ALL_MODULES.items():
        print(a_module, expect_operator)
        # For example: TestVersionedDivTensorExampleV7
        torch_module_name = type(a_module).__name__

        # The corresponding model name is: test_versioned_div_tensor_example_v4
        model_name = ''.join([
            '_' + char.lower() if char.isupper() else char for char in torch_module_name
        ]).lstrip('_')

        # Some models may not compile anymore, so skip the ones
        # that already has pt file for them.
        logger.info(f"Processing {torch_module_name}")
        if model_exist(model_name, all_models):
            logger.info(f"Model {model_name} already exists, skipping")
            continue

        script_module = torch.jit.script(a_module)
        actual_model_version = get_output_model_version(script_module)

        current_operator_version = torch._C._get_max_operator_version()
        if actual_model_version >= current_operator_version + 1:
            logger.error(
                f"Actual model version {actual_model_version} "
                f"is equal or larger than {current_operator_version} + 1. "
                f"Please run the script before the commit to change operator.")
            continue

        actual_operator_list = get_operator_list(script_module)
        if expect_operator not in actual_operator_list:
            logger.error(
                f"The model includes operator: {actual_operator_list}, "
                f"however it doesn't cover the operator {expect_operator}."
                f"Please ensure the output model includes the tested operator.")
            continue

        export_model_path = str(model_directory_path / (str(model_name) + ".ptl"))
        script_module._save_for_lite_interpreter(export_model_path)
        logger.info(f"Generating model {model_name} and it's save to {export_model_path}")
