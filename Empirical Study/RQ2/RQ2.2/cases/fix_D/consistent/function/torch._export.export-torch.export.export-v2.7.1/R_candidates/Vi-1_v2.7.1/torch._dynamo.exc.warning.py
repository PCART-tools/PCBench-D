def warning(msg: str) -> None:
    counters["warnings"][msg] += 1
    assert msg != os.environ.get("BREAK", False)
