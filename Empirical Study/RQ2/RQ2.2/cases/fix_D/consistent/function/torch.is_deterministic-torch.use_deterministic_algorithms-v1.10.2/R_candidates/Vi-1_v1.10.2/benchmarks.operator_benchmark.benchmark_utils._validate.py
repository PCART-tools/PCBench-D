def _validate(configs):
    """ Validate inputs from users."""
    if 'device' in configs:
        for v in configs['device']:
            assert(v in _supported_devices), "Device needs to be a string."
