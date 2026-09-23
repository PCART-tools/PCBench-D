    def _repr_html_(self):
        """IPython display hook for rendering."""
        fmt = mpl.rcParams['animation.html']
        if fmt == 'html5':
            return self.to_html5_video()
        elif fmt == 'jshtml':
            return self.to_jshtml()
