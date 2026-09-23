    def _update_prop(self, legend_handle, orig_handle):
        def first_color(colors):
            if colors is None:
                return None
            colors = mcolors.to_rgba_array(colors)
            if len(colors):
                return colors[0]
            else:
                return "none"
        def get_first(prop_array):
            if len(prop_array):
                return prop_array[0]
            else:
                return None
        edgecolor = getattr(orig_handle, '_original_edgecolor',
                            orig_handle.get_edgecolor())
        legend_handle.set_edgecolor(first_color(edgecolor))
        facecolor = getattr(orig_handle, '_original_facecolor',
                            orig_handle.get_facecolor())
        legend_handle.set_facecolor(first_color(facecolor))
        legend_handle.set_fill(orig_handle.get_fill())
        legend_handle.set_hatch(orig_handle.get_hatch())
        legend_handle.set_linewidth(get_first(orig_handle.get_linewidths()))
        legend_handle.set_linestyle(get_first(orig_handle.get_linestyles()))
        legend_handle.set_transform(get_first(orig_handle.get_transforms()))
        legend_handle.set_figure(orig_handle.get_figure())
        legend_handle.set_alpha(orig_handle.get_alpha())
