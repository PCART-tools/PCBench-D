def check_args_exist(target_type) -> None:
    if target_type is List or target_type is list:
        raise_error_container_parameter_missing("List")
    elif target_type is Tuple or target_type is tuple:
        raise_error_container_parameter_missing("Tuple")
    elif target_type is Dict or target_type is dict:
        raise_error_container_parameter_missing("Dict")
    elif target_type is None or target_type is Optional:
        raise_error_container_parameter_missing("Optional")
