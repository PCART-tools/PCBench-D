@composite
def strategy_decimal(draw: DrawFn) -> PyDecimal:
    """Draw a decimal value, varying the number of decimal places."""
    places = draw(integers(min_value=0, max_value=18))
    return draw(
        # TODO: once fixed, re-enable decimal nan/inf values...
        #  (see https://github.com/pola-rs/polars/issues/8421)
        decimals(
            allow_nan=False,
            allow_infinity=False,
            min_value=-(2**66),
            max_value=(2**66) - 1,
            places=places,
        )
    )
