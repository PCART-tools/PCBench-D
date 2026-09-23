    @cbook.deprecated("3.2", alternative="ax.get_subplotspec().rowspan.start")
    @property
    def rowNum(self):
        return self.get_subplotspec().rowspan.start
