    def _to_latex_via_styler(
        self,
        buf=None,
        *,
        hide: dict | list[dict] | None = None,
        relabel_index: dict | list[dict] | None = None,
        format: dict | list[dict] | None = None,
        format_index: dict | list[dict] | None = None,
        render_kwargs: dict | None = None,
    ):
        """
        Render object to a LaTeX tabular, longtable, or nested table.

        Uses the ``Styler`` implementation with the following, ordered, method chaining:

        .. code-block:: python
           styler = Styler(DataFrame)
           styler.hide(**hide)
           styler.relabel_index(**relabel_index)
           styler.format(**format)
           styler.format_index(**format_index)
           styler.to_latex(buf=buf, **render_kwargs)

        Parameters
        ----------
        buf : str, Path or StringIO-like, optional, default None
            Buffer to write to. If None, the output is returned as a string.
        hide : dict, list of dict
            Keyword args to pass to the method call of ``Styler.hide``. If a list will
            call the method numerous times.
        relabel_index : dict, list of dict
            Keyword args to pass to the method of ``Styler.relabel_index``. If a list
            will call the method numerous times.
        format : dict, list of dict
            Keyword args to pass to the method call of ``Styler.format``. If a list will
            call the method numerous times.
        format_index : dict, list of dict
            Keyword args to pass to the method call of ``Styler.format_index``. If a
            list will call the method numerous times.
        render_kwargs : dict
            Keyword args to pass to the method call of ``Styler.to_latex``.

        Returns
        -------
        str or None
            If buf is None, returns the result as a string. Otherwise returns None.
        """
        from pandas.io.formats.style import Styler

        self = cast("DataFrame", self)
        styler = Styler(self, uuid="")

        for kw_name in ["hide", "relabel_index", "format", "format_index"]:
            kw = vars()[kw_name]
            if isinstance(kw, dict):
                getattr(styler, kw_name)(**kw)
            elif isinstance(kw, list):
                for sub_kw in kw:
                    getattr(styler, kw_name)(**sub_kw)

        # bold_rows is not a direct kwarg of Styler.to_latex
        render_kwargs = {} if render_kwargs is None else render_kwargs
        if render_kwargs.pop("bold_rows"):
            styler.applymap_index(lambda v: "textbf:--rwrap;")

        return styler.to_latex(buf=buf, **render_kwargs)
