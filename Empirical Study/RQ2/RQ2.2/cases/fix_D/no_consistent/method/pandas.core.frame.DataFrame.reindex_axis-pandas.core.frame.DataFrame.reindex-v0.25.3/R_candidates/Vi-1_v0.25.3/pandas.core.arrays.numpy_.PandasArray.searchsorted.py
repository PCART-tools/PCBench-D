    @Appender(ExtensionArray.searchsorted.__doc__)
    def searchsorted(self, value, side="left", sorter=None):
        return searchsorted(self.to_numpy(), value, side=side, sorter=sorter)
