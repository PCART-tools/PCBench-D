    def set_label(self, label, *, loc=None, **kwargs):
        """Add a label to the long axis of the colorbar."""
        _pos_xy = 'y' if self.orientation == 'vertical' else 'x'
        _protected_kw = [_pos_xy, 'horizontalalignment', 'ha']
        if any([k in kwargs for k in _protected_kw]):
            if loc is not None:
                raise TypeError(f'Specifying *loc* is disallowed when any of '
                                f'its corresponding low level keyword '
                                f'arguments {_protected_kw} are also supplied')
            loc = 'center'
        else:
            if loc is None:
                loc = mpl.rcParams['%saxis.labellocation' % _pos_xy]
        if self.orientation == 'vertical':
            cbook._check_in_list(('bottom', 'center', 'top'), loc=loc)
        else:
            cbook._check_in_list(('left', 'center', 'right'), loc=loc)
        if loc in ['right', 'top']:
            kwargs[_pos_xy] = 1.
            kwargs['horizontalalignment'] = 'right'
        elif loc in ['left', 'bottom']:
            kwargs[_pos_xy] = 0.
            kwargs['horizontalalignment'] = 'left'
        self._label = label
        self._labelkw = kwargs
        self._set_label()
