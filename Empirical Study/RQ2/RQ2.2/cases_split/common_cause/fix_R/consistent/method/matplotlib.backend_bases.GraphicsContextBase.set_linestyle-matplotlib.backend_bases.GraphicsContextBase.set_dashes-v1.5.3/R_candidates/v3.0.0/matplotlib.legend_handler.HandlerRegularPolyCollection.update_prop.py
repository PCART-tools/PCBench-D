    def update_prop(self, legend_handle, orig_handle, legend):

        self._update_prop(legend_handle, orig_handle)

        legend_handle.set_figure(legend.figure)
        #legend._set_artist_props(legend_handle)
        legend_handle.set_clip_box(None)
        legend_handle.set_clip_path(None)
