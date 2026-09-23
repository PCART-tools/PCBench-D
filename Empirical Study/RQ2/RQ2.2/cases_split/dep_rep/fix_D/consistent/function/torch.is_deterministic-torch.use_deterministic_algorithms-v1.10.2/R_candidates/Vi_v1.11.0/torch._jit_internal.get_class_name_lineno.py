def get_class_name_lineno(method) -> Tuple[str, int]:
    current_frame = inspect.currentframe()

    # one for the get_class_name call, one for _overload_method call
    for i in range(2):
        assert current_frame is not None  # assert current frame is not an Optional[FrameType]
        current_frame = current_frame.f_back

    assert current_frame is not None  # same here
    class_name = current_frame.f_code.co_name
    line_no = current_frame.f_code.co_firstlineno
    return class_name, line_no
