    def update_ticks(self):
        """
        Force the update of the ticks and ticklabels. This must be
        called whenever the tick locator and/or tick formatter changes.
        """
        ax = self.ax
        ticks, ticklabels, offset_string = self._ticker()
        if self.orientation == 'vertical':
            ax.yaxis.set_ticks(ticks)
            ax.set_yticklabels(ticklabels)
            ax.yaxis.get_major_formatter().set_offset_string(offset_string)

        else:
            ax.xaxis.set_ticks(ticks)
            ax.set_xticklabels(ticklabels)
            ax.xaxis.get_major_formatter().set_offset_string(offset_string)
