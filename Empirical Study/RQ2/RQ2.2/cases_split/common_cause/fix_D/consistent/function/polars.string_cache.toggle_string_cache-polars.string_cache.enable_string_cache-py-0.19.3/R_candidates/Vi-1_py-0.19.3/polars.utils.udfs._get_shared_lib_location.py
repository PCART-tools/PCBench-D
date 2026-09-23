def _get_shared_lib_location(main_file: Any) -> str:
    import os

    directory = os.path.dirname(main_file)  # noqa: PTH120
    return os.path.join(  # noqa: PTH118
        directory, next(filter(is_shared_lib, os.listdir(directory)))
    )
