    def __init__(
        self,
        row: int,
        col: int,
        val,
        style: dict | None,
        css_styles: dict[tuple[int, int], list[tuple[str, Any]]] | None,
        css_row: int,
        css_col: int,
        css_converter: Callable | None,
        **kwargs,
    ):
        if css_styles and css_converter:
            css = ";".join(a + ":" + str(v) for (a, v) in css_styles[css_row, css_col])
            style = css_converter(css)

        return super().__init__(row=row, col=col, val=val, style=style, **kwargs)
