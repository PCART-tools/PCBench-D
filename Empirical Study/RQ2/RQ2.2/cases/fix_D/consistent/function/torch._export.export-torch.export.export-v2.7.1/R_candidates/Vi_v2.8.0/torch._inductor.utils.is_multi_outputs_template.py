def is_multi_outputs_template(input_buf: Optional[Union[Buffer, Operation]]) -> bool:
    """
    Check if input buffer is a multi-outputs template buffer
    """
    from . import ir

    return isinstance(input_buf, ir.CppTemplateBuffer) and isinstance(
        input_buf.layout, ir.MultiOutputLayout
    )
