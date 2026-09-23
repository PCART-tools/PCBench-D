def _nums_to_str(*args):
    return " ".join(f"{arg:1.3f}".rstrip("0").rstrip(".") for arg in args)
