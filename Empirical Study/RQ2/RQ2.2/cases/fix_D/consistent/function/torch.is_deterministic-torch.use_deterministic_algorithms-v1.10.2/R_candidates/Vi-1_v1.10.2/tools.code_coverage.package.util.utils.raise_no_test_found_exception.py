def raise_no_test_found_exception(
    cpp_binary_folder: str, python_binary_folder: str
) -> NoReturn:
    raise RuntimeError(
        f"No cpp and python tests found in folder **{cpp_binary_folder} and **{python_binary_folder}**"
    )
