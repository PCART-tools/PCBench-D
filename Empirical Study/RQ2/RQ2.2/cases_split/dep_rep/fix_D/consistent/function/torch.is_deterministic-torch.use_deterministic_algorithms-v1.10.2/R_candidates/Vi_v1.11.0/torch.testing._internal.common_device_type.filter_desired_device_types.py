def filter_desired_device_types(device_type_test_bases, except_for=None, only_for=None):
    # device type cannot appear in both except_for and only_for
    intersect = set(except_for if except_for else []) & set(only_for if only_for else [])
    assert not intersect, f"device ({intersect}) appeared in both except_for and only_for"

    if except_for:
        device_type_test_bases = filter(
            lambda x: x.device_type not in except_for, device_type_test_bases)
    if only_for:
        device_type_test_bases = filter(
            lambda x: x.device_type in only_for, device_type_test_bases)

    return list(device_type_test_bases)
