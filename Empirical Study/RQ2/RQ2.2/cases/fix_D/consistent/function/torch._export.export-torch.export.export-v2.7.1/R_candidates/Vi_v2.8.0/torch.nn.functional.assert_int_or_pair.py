def assert_int_or_pair(arg: list[int], arg_name: str, message: str) -> None:
    assert isinstance(arg, int) or len(arg) == 2, message.format(arg_name)
