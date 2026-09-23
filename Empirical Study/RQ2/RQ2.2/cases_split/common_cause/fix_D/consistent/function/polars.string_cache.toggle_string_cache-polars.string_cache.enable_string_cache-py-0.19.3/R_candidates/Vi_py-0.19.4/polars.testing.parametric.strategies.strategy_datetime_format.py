@composite
def strategy_datetime_format(draw: DrawFn) -> str:
    """Draw a random datetime format string."""
    fmt = draw(
        sets(
            sampled_from(
                [
                    "%m",
                    "%b",
                    "%B",
                    "%d",
                    "%j",
                    "%a",
                    "%A",
                    "%w",
                    "%H",
                    "%I",
                    "%p",
                    "%M",
                    "%S",
                    "%U",
                    "%W",
                    "%%",
                ]
            ),
        )
    )

    # Make sure year is always present
    fmt.add("%Y")

    return " ".join(fmt)
