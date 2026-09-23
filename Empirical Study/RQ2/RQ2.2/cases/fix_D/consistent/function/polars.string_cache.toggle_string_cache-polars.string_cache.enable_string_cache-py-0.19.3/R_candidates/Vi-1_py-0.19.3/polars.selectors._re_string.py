def _re_string(string: str | Collection[str]) -> str:
    """Return escaped regex, potentially representing multiple string fragments."""
    if isinstance(string, str):
        rx = f"{re.escape(string)}"
    else:
        strings: list[str] = []
        for st in string:
            if isinstance(st, Collection) and not isinstance(st, str):  # type: ignore[redundant-expr]
                strings.extend(st)
            else:
                strings.append(st)
        rx = "|".join(re.escape(x) for x in strings)
    return f"({rx})"
