    def get_legend_handles_labels(self, legend_handler_map=None):
        """
        Return handles and labels for legend

        ``ax.legend()`` is equivalent to ::

          h, l = ax.get_legend_handles_labels()
          ax.legend(h, l)

        """
        handles = []
        labels = []
        for handle in self._get_legend_handles(legend_handler_map):
            label = handle.get_label()
            if label and not label.startswith('_'):
                handles.append(handle)
                labels.append(label)

        return handles, labels
