    def _copy_collection_props(self, legend_handle, orig_handle):
        """
        Copy properties from the `.LineCollection` *orig_handle* to the
        `.Line2D` *legend_handle*.
        """
        legend_handle.set_color(orig_handle.get_color()[0])
        legend_handle.set_linestyle(orig_handle.get_linestyle()[0])
