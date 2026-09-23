    @_api.deprecated("3.7", alternative=(
        "[cs.labelTexts[0].get_font().get_size()] * len(cs.labelLevelList)"))
    @property
    def labelFontSizeList(self):
        return [self._label_font_props.get_size()] * len(self.labelLevelList)
