def _duration_to_dtype(dtype: Duration) -> Dtype:
    tu = dtype.time_unit[0] if dtype.time_unit is not None else "u"
    arrow_c_type = f"tD{tu}"
    return DtypeKind.DATETIME, 64, arrow_c_type, NE
