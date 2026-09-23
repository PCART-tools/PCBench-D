def _parse_size(size_str):
    """Convert memory size strings ('12 GB' etc.) to float"""
    suffixes = {
        "": 1,
        "b": 1,
        "k": 1000,
        "m": 1000**2,
        "g": 1000**3,
        "t": 1000**4,
        "kb": 1000,
        "mb": 1000**2,
        "gb": 1000**3,
        "tb": 1000**4,
        "kib": 1024,
        "mib": 1024**2,
        "gib": 1024**3,
        "tib": 1024**4,
    }

    size_re = re.compile(
        r"^\s*(\d+|\d+\.\d+)\s*({})\s*$".format("|".join(suffixes.keys())),
        re.IGNORECASE,
    )

    m = size_re.match(size_str.lower())
    if not m or m.group(2) not in suffixes:
        raise ValueError(f"value {size_str!r} not a valid size")
    return int(float(m.group(1)) * suffixes[m.group(2)])
