def get_pytorch_folder() -> str:
    # TOOLS_FOLDER in oss: pytorch/tools/code_coverage
    return os.path.abspath(
        os.environ.get(
            "PYTORCH_FOLDER", os.path.join(TOOLS_FOLDER, os.path.pardir, os.path.pardir)
        )
    )
