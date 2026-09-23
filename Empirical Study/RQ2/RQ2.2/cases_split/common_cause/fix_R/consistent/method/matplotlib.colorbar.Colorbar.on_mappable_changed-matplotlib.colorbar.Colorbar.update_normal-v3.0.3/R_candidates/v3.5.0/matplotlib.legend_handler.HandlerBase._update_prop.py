    def _update_prop(self, legend_handle, orig_handle):
        if self._update_prop_func is None:
            self._default_update_prop(legend_handle, orig_handle)
        else:
            self._update_prop_func(legend_handle, orig_handle)
