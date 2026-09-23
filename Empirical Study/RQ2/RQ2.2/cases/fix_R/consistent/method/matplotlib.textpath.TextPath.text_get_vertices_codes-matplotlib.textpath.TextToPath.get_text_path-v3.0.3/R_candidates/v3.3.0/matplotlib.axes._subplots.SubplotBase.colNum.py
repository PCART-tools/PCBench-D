    @cbook.deprecated("3.2", alternative="ax.get_subplotspec().colspan.start")
    @property
    def colNum(self):
        return self.get_subplotspec().colspan.start
