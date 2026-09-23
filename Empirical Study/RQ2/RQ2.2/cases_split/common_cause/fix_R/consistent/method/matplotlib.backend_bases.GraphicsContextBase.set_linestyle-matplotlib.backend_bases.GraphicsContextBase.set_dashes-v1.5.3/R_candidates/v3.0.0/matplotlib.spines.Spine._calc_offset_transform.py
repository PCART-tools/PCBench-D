    def _calc_offset_transform(self):
        """calculate the offset transform performed by the spine"""
        self._ensure_position_is_set()
        position = self._position
        if isinstance(position, str):
            if position == 'center':
                position = ('axes', 0.5)
            elif position == 'zero':
                position = ('data', 0)
        assert len(position) == 2, "position should be 2-tuple"
        position_type, amount = position
        assert position_type in ('axes', 'outward', 'data')
        if position_type == 'outward':
            if amount == 0:
                # short circuit commonest case
                self._spine_transform = ('identity',
                                         mtransforms.IdentityTransform())
            elif self.spine_type in ['left', 'right', 'top', 'bottom']:
                offset_vec = {'left': (-1, 0),
                              'right': (1, 0),
                              'bottom': (0, -1),
                              'top': (0, 1),
                              }[self.spine_type]
                # calculate x and y offset in dots
                offset_x = amount * offset_vec[0] / 72.0
                offset_y = amount * offset_vec[1] / 72.0
                self._spine_transform = ('post',
                                         mtransforms.ScaledTranslation(
                                             offset_x,
                                             offset_y,
                                             self.figure.dpi_scale_trans))
            else:
                warnings.warn('unknown spine type "%s": no spine '
                              'offset performed' % self.spine_type)
                self._spine_transform = ('identity',
                                         mtransforms.IdentityTransform())
        elif position_type == 'axes':
            if self.spine_type in ('left', 'right'):
                self._spine_transform = ('pre',
                                         mtransforms.Affine2D.from_values(
                                             # keep y unchanged, fix x at
                                             # amount
                                             0, 0, 0, 1, amount, 0))
            elif self.spine_type in ('bottom', 'top'):
                self._spine_transform = ('pre',
                                         mtransforms.Affine2D.from_values(
                                             # keep x unchanged, fix y at
                                             # amount
                                             1, 0, 0, 0, 0, amount))
            else:
                warnings.warn('unknown spine type "%s": no spine '
                              'offset performed' % self.spine_type)
                self._spine_transform = ('identity',
                                         mtransforms.IdentityTransform())
        elif position_type == 'data':
            if self.spine_type in ('right', 'top'):
                # The right and top spines have a default position of 1 in
                # axes coordinates.  When specifying the position in data
                # coordinates, we need to calculate the position relative to 0.
                amount -= 1
            if self.spine_type in ('left', 'right'):
                self._spine_transform = ('data',
                                         mtransforms.Affine2D().translate(
                                             amount, 0))
            elif self.spine_type in ('bottom', 'top'):
                self._spine_transform = ('data',
                                         mtransforms.Affine2D().translate(
                                             0, amount))
            else:
                warnings.warn('unknown spine type "%s": no spine '
                              'offset performed' % self.spine_type)
                self._spine_transform = ('identity',
                                         mtransforms.IdentityTransform())
