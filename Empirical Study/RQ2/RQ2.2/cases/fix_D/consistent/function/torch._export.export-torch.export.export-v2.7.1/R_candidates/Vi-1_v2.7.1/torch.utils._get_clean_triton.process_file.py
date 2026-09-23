def process_file(input_filename: str, output_filename: str) -> str:
    with open(input_filename) as file:
        source_code = file.read()

    transformed_code = source_code
    if "def triton_(" in source_code:
        raise RuntimeError(
            "Need to run original Pytorch code generating kernels with TORCHINDUCTOR_UNIQUE_KERNEL_NAMES=1"
        )
    # transformed_code = rename_kernels(transformed_code)
    transformed_code = remove_triton_function_declaration(transformed_code)
    transformed_code = remove_async_compile(transformed_code)

    launch_params_filename = f"{input_filename}.launch_params"
    if not os.path.exists(launch_params_filename):
        raise RuntimeError(
            f"Missing {launch_params_filename}. Run `TORCHINDUCTOR_DUMP_LAUNCH_PARAMS=1 python {input_filename} first."
        )

    with open(launch_params_filename) as f:
        launch_params_meta = f.readlines()

    split_params = [i.split("|") for i in launch_params_meta]
    kernel_args_grid = {a.strip(): (b.strip(), c.strip()) for a, b, c in split_params}
    transformed_code = add_launch_params(transformed_code, kernel_args_grid)

    with open(output_filename, "w") as file:
        file.write(transformed_code)
    return transformed_code
