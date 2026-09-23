    def set_adjustable(self, adjustable):
        """
        ACCEPTS: [ 'box' | 'datalim' | 'box-forced']
        """
        if adjustable in ('box', 'datalim', 'box-forced'):
            if self in self._shared_x_axes or self in self._shared_y_axes:
                if adjustable == 'box':
                    raise ValueError(
                        'adjustable must be "datalim" for shared axes')
            self._adjustable = adjustable
        else:
            raise ValueError('argument must be "box", or "datalim"')
        self.stale = True
