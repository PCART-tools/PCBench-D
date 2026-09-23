@deprecate_function(
    message="This function has been superseded by `expand_selector`; please update accordingly",
    version="0.18.14",
)
def selector_column_names(
    frame: DataFrame | LazyFrame, selector: SelectorType
) -> tuple[str, ...]:
    """
    Return the column names that would be selected from the given frame.

    .. deprecated:: 0.18.14
       Use :func:`expand_selector` instead.

    Parameters
    ----------
    frame
        A polars DataFrame or LazyFrame.
    selector
        An arbitrary polars selector (or compound selector).

    """
    return expand_selector(target=frame, selector=selector)
