def _check_arg_is_1byte(
    arg_name: str, arg: str | None, can_be_empty: bool = False
) -> None:
    if isinstance(arg, str):
        arg_byte_length = len(arg.encode("utf-8"))
        if can_be_empty:
            if arg_byte_length > 1:
                raise ValueError(
                    f'{arg_name}="{arg}" should be a single byte character or empty,'
                    f" but is {arg_byte_length} bytes long."
                )
        elif arg_byte_length != 1:
            raise ValueError(
                f'{arg_name}="{arg}" should be a single byte character, but is'
                f" {arg_byte_length} bytes long."
            )
