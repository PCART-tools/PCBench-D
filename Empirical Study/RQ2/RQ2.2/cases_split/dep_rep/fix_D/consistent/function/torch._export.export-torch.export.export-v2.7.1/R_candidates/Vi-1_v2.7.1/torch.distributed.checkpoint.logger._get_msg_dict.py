def _get_msg_dict(func_name, *args, **kwargs) -> dict[str, Any]:
    msg_dict = _msg_dict_from_dcp_method_args(*args, **kwargs)
    msg_dict.update(c10d_logger._get_msg_dict(func_name, *args, **kwargs))

    return msg_dict
