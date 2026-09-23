    def _render_latex(
        self, sparse_index: bool, sparse_columns: bool, clines: str | None, **kwargs
    ) -> str:
        """
        Render a Styler in latex format
        """
        d = self._render(sparse_index, sparse_columns, None, None)
        self._translate_latex(d, clines=clines)
        self.template_latex.globals["parse_wrap"] = _parse_latex_table_wrapping
        self.template_latex.globals["parse_table"] = _parse_latex_table_styles
        self.template_latex.globals["parse_cell"] = _parse_latex_cell_styles
        self.template_latex.globals["parse_header"] = _parse_latex_header_span
        d.update(kwargs)
        return self.template_latex.render(**d)
