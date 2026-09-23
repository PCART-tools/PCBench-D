def get_operator_list(script_module: torch) -> Set[str]:
    buffer = io.BytesIO(script_module._save_to_buffer_for_lite_interpreter())
    buffer.seek(0)
    mobile_module = _load_for_lite_interpreter(buffer)
    operator_list = _export_operator_list(mobile_module)
    return operator_list
