def tabulate(
    rows: Union[list[tuple[str, object]], list[list[object]]],
    headers: Union[tuple[str, ...], list[str]],
) -> str:
    try:
        import tabulate

        return tabulate.tabulate(rows, headers=headers)
    except ImportError:
        return "\n".join(
            ", ".join(map(str, row)) for row in itertools.chain([headers], rows)
        )
