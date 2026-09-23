    @cbook.deprecated("3.2",
                      alternative="self.GetTopLevelParent().GetStatusBar()")
    @property
    def statbar(self):
        return self.GetTopLevelParent().GetStatusBar()
