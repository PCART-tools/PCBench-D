    def _adjust_frame_size(self):
        if self.codec == 'h264':
            wo, ho = self.fig.get_size_inches()
            w, h = adjusted_figsize(wo, ho, self.dpi, 2)
            if not (wo, ho) == (w, h):
                self.fig.set_size_inches(w, h, forward=True)
                verbose.report('figure size (inches) has been adjusted '
                               'from %s x %s to %s x %s' % (wo, ho, w, h),
                               level='helpful')
        else:
            w, h = self.fig.get_size_inches()
        verbose.report('frame size in pixels is %s x %s' % self.frame_size,
                       level='debug')
        return w, h
