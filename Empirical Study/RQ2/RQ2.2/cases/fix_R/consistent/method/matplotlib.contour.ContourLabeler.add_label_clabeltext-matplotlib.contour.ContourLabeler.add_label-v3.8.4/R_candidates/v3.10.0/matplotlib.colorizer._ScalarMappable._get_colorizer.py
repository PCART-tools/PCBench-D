    @staticmethod
    def _get_colorizer(cmap, norm, colorizer):
        if isinstance(colorizer, Colorizer):
            _ScalarMappable._check_exclusionary_keywords(
                Colorizer, cmap=cmap, norm=norm
            )
            return colorizer
        return Colorizer(cmap, norm)
