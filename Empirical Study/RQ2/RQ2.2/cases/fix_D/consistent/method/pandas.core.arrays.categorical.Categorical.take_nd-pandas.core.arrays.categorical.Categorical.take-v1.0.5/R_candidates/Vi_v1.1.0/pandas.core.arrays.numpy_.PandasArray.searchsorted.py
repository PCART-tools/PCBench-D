    @doc(ExtensionArray.searchsorted)
    def searchsorted(self, value, side="left", sorter=None):
        return searchsorted(self.to_numpy(), value, side=side, sorter=sorter)
