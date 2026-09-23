def get_num_sms() -> int:
    """Handle experimental carveout if set otherwise return hardware SM count"""
    # TODO we need to properly guard on this global
    carveout = torch._C._get_sm_carveout_experimental()
    return get_max_num_sms() - (carveout if carveout is not None else 0)
