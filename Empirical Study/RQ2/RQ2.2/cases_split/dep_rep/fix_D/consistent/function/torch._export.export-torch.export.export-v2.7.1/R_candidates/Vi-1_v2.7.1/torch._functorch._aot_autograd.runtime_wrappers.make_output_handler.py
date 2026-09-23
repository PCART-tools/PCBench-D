def make_output_handler(info, runtime_metadata, trace_joint):
    handler_type = _HANDLER_MAP[info.output_type]
    return handler_type(info, runtime_metadata, trace_joint)
