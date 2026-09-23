def positive_integer(value: str) -> float:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError(f"{value} is not a natural number")
    return parsed
