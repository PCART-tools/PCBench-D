    def get_kern(self, font1: str, fontclass1: str, sym1: str, fontsize1: float,
                 font2: str, fontclass2: str, sym2: str, fontsize2: float,
                 dpi: float) -> float:
        """
        Get the kerning distance for font between *sym1* and *sym2*.

        See `~.Fonts.get_metrics` for a detailed description of the parameters.
        """
        return 0.
