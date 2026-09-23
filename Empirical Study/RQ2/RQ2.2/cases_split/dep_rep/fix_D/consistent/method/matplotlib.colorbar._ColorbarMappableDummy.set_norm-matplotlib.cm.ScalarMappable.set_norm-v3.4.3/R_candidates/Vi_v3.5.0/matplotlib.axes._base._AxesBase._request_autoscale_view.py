    def _request_autoscale_view(self, tight=None, **kwargs):
        # kwargs are "scalex", "scaley" (& "scalez" for 3D) and default to True
        want_scale = {name: True for name in self._axis_names}
        for k, v in kwargs.items():  # Validate args before changing anything.
            if k.startswith("scale"):
                name = k[5:]
                if name in want_scale:
                    want_scale[name] = v
                    continue
            raise TypeError(
                f"_request_autoscale_view() got an unexpected argument {k!r}")
        if tight is not None:
            self._tight = tight
        for k, v in want_scale.items():
            if v:
                self._stale_viewlims[k] = True  # Else keep old state.
