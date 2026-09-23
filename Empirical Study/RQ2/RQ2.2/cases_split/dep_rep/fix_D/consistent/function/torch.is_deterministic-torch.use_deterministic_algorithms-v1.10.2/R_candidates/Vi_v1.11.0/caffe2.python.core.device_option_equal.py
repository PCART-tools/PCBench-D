def device_option_equal(opt1, opt2, ignore_node_name=True, ignore_random_seed=True):
    if not opt1 or not opt2:
        return opt1 == opt2
    if not ignore_node_name and opt1.node_name != opt2.node_name:
        return False
    if not ignore_random_seed and opt1.random_seed != opt2.random_seed:
        return False
    if not opt1.device_type or not opt2.device_type:
        # At least one option is for CPU, check if both are for CPU.
        return not opt1.device_type and not opt2.device_type
    return opt1.device_id == opt2.device_id
