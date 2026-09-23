    def remove(self):
        """
        Remove this colorbar from the figure
        """

        fig = self.ax.figure
        fig.delaxes(self.ax)
