def parse_value(value: str) -> Any:
    # Take the value from a line of `sccache --show-stats` and try to parse
    # out a value
    try:
        return int(value)
    except ValueError:
        # sccache reports times as 0.000 s, so detect that here and strip
        # off the non-numeric parts
        if value.endswith(" s"):
            return float(value[: -len(" s")])

    return value
