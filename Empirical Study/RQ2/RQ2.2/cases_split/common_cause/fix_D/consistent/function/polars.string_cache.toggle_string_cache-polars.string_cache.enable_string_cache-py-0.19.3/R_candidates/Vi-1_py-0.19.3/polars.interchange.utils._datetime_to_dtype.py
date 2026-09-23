def _datetime_to_dtype(dtype: Datetime) -> Dtype:
    tu = dtype.time_unit[0] if dtype.time_unit is not None else "u"
    tz = dtype.time_zone if dtype.time_zone is not None else ""
    arrow_c_type = f"ts{tu}:{tz}"
    return DtypeKind.DATETIME, 64, arrow_c_type, NE
