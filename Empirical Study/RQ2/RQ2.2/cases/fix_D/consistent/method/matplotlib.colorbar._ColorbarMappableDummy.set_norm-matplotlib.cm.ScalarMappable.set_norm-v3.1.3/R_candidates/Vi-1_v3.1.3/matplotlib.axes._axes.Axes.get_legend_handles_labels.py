    def get_legend_handles_labels(self, legend_handler_map=None):
        """
        Return handles and labels for legend

        ``ax.legend()`` is equivalent to ::

          h, l = ax.get_legend_handles_labels()
          ax.legend(h, l)

        """

        # pass through to legend.
        handles, labels = mlegend._get_legend_handles_labels([self],
                legend_handler_map)
        return handles, labels
