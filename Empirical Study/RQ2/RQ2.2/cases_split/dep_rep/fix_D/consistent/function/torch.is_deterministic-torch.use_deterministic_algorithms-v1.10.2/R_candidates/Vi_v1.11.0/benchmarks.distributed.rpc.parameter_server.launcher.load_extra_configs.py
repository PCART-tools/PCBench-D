def load_extra_configs(args):
    r"""
    A function that creates a dictionary that contains any extra configurations
    set by the user. The dictionary will contain two keys trainer_config and
    server_config, with default values None.
    Args:
        args (parser): launcher configurations
    """
    trainer_config_file = args.trainer_config_path
    server_config_file = args.server_config_path
    configurations = {
        "trainer_config": None,
        "server_config": None
    }
    if args.trainer is not None and trainer_config_file is not None:
        configurations["trainer_config"] = get_json_config(trainer_config_file, args.trainer)
    if args.server is not None and server_config_file is not None:
        configurations["server_config"] = get_json_config(server_config_file, args.server)
    return configurations
