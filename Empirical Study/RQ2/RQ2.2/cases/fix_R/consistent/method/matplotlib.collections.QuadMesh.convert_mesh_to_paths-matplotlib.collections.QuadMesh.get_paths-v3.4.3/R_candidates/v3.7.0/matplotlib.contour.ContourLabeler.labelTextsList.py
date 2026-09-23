    @_api.deprecated("3.7", alternative="cs.labelTexts")
    @property
    def labelTextsList(self):
        return cbook.silent_list('text.Text', self.labelTexts)
