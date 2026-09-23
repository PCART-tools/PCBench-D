def _construct_series_with_fallbacks(
    constructor: Callable[[str, Sequence[Any], bool], PySeries],
    name: str,
    values: Sequence[Any],
    target_dtype: PolarsDataType | None,
    *,
    strict: bool,
) -> PySeries:
    """Construct Series, with fallbacks for basic type mismatch (eg: bool/int)."""
    while True:
        try:
            return constructor(name, values, strict)
        except TypeError as exc:
            str_exc = str(exc)

            # from x to float
            # error message can be:
            #   - integers: "'float' object cannot be interpreted as an integer"
            if "'float'" in str_exc and (
                # we do not accept float values as int/temporal, as it causes silent
                # information loss; the caller should explicitly cast in this case.
                target_dtype
                not in (INTEGER_DTYPES | TEMPORAL_DTYPES)
            ):
                constructor = py_type_to_constructor(float)

            # from x to string
            # error message can be:
            #   - integers: "'str' object cannot be interpreted as an integer"
            #   - floats: "must be real number, not str"
            elif "'str'" in str_exc or str_exc == "must be real number, not str":
                constructor = py_type_to_constructor(str)

            # from x to int
            # error message can be:
            #   - bools: "'int' object cannot be converted to 'PyBool'"
            elif str_exc == "'int' object cannot be converted to 'PyBool'":
                constructor = py_type_to_constructor(int)

            elif "decimal.Decimal" in str_exc:
                constructor = py_type_to_constructor(PyDecimal)
            else:
                raise
