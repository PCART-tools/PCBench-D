    @cbook.deprecated("3.3", alternative="matplotlib.get_cachedir()")
    @property
    def cachedir(self):
        return mpl.get_cachedir()
