def filter_desired_device_types(device_type_test_bases, except_for=None, only_for=None):
    # device type cannot appear in both except_for and only_for
    intersect = set(except_for if except_for else []) & set(
        only_for if only_for else []
    )
    assert (
        not intersect
    ), f"device ({intersect}) appeared in both except_for and only_for"

    # Replace your privateuse1 backend name with 'privateuse1'
    if is_privateuse1_backend_available():
        privateuse1_backend_name = torch._C._get_privateuse1_backend_name()
        except_for = (
            ["privateuse1" if x == privateuse1_backend_name else x for x in except_for]
            if except_for is not None
            else None
        )
        only_for = (
            ["privateuse1" if x == privateuse1_backend_name else x for x in only_for]
            if only_for is not None
            else None
        )

    if except_for:
        device_type_test_bases = filter(
            lambda x: x.device_type not in except_for, device_type_test_bases
        )
    if only_for:
        device_type_test_bases = filter(
            lambda x: x.device_type in only_for, device_type_test_bases
        )

    return list(device_type_test_bases)
