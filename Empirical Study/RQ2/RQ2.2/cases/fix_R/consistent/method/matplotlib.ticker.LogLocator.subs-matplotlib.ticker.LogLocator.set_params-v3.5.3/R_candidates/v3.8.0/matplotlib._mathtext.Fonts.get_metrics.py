    def get_metrics(self, font: str, font_class: str, sym: str, fontsize: float,
                    dpi: float) -> FontMetrics:
        r"""
        Parameters
        ----------
        font : str
            One of the TeX font names: "tt", "it", "rm", "cal", "sf", "bf",
            "default", "regular", "bb", "frak", "scr".  "default" and "regular"
            are synonyms and use the non-math font.
        font_class : str
            One of the TeX font names (as for *font*), but **not** "bb",
            "frak", or "scr".  This is used to combine two font classes.  The
            only supported combination currently is ``get_metrics("frak", "bf",
            ...)``.
        sym : str
            A symbol in raw TeX form, e.g., "1", "x", or "\sigma".
        fontsize : float
            Font size in points.
        dpi : float
            Rendering dots-per-inch.

        Returns
        -------
        FontMetrics
        """
        info = self._get_info(font, font_class, sym, fontsize, dpi)
        return info.metrics
