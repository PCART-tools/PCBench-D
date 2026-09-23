    def _default_update_prop(self, legend_handle, orig_handle):
        lw = orig_handle.get_linewidths()[0]
        dashes = orig_handle._us_linestyles[0]
        color = orig_handle.get_colors()[0]
        legend_handle.set_color(color)
        legend_handle.set_linestyle(dashes)
        legend_handle.set_linewidth(lw)
