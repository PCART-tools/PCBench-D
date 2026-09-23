def _handle_columns_arg(
    data: list[PySeries],
    columns: Sequence[str] | None = None,
    *,
    from_dict: bool = False,
) -> list[PySeries]:
    """Rename data according to columns argument."""
    if not columns:
        return data
    else:
        if not data:
            return [pl.Series(c, None)._s for c in columns]
        elif len(data) == len(columns):
            if from_dict:
                series_map = {s.name(): s for s in data}
                if all((col in series_map) for col in columns):
                    return [series_map[col] for col in columns]
            for i, c in enumerate(columns):
                if c != data[i].name():
                    data[i] = data[i].clone()
                    data[i].rename(c)
            return data
        else:
            raise ValueError("dimensions of columns arg must match data dimensions")
