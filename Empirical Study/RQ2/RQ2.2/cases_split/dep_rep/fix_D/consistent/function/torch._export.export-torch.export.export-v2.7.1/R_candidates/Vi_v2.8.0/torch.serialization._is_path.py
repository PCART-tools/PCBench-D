def _is_path(name_or_buffer: object) -> TypeIs[Union[str, os.PathLike]]:
    return isinstance(name_or_buffer, (str, os.PathLike))
