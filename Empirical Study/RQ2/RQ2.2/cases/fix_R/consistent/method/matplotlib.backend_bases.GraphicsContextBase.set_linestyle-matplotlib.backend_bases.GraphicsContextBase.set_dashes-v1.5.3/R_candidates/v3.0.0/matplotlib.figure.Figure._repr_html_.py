    def _repr_html_(self):
        # We can't use "isinstance" here, because then we'd end up importing
        # webagg unconditiionally.
        if (self.canvas is not None and
                'WebAgg' in self.canvas.__class__.__name__):
            from matplotlib.backends import backend_webagg
            return backend_webagg.ipython_inline_display(self)
