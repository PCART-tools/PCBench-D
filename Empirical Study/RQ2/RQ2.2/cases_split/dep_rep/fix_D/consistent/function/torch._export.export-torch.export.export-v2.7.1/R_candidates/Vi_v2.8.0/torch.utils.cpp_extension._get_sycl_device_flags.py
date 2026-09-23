def _get_sycl_device_flags(cflags):
    # We need last occurence of -fsycl-targets as it will be the one taking effect.
    # So searching in reversed list.
    flags = [f for f in reversed(cflags) if f.startswith('-fsycl-targets=')]
    assert flags, "bug: -fsycl-targets should have been ammended to cflags"

    arch_list = _get_sycl_arch_list()
    if arch_list != '':
        flags += [f'-Xs "-device {arch_list}"']
    return flags
