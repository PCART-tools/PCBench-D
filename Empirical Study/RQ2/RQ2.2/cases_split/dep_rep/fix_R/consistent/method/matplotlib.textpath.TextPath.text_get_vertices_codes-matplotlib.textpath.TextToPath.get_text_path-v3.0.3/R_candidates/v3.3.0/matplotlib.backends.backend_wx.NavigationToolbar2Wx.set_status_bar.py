    @cbook.deprecated("3.2")
    def set_status_bar(self, statbar):
        self.GetTopLevelParent().SetStatusBar(statbar)
