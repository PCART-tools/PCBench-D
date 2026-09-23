    def get_spine_transform(self):
        """Return the spine transform."""
        self._ensure_position_is_set()
        what, how = self._spine_transform

        if what == 'data':
            # special case data based spine locations
            data_xform = self.axes.transScale + \
                (how + self.axes.transLimits + self.axes.transAxes)
            if self.spine_type in ['left', 'right']:
                result = mtransforms.blended_transform_factory(
                    data_xform, self.axes.transData)
            elif self.spine_type in ['top', 'bottom']:
                result = mtransforms.blended_transform_factory(
                    self.axes.transData, data_xform)
            else:
                raise ValueError('unknown spine spine_type: %s' %
                                 self.spine_type)
            return result

        if self.spine_type in ['left', 'right']:
            base_transform = self.axes.get_yaxis_transform(which='grid')
        elif self.spine_type in ['top', 'bottom']:
            base_transform = self.axes.get_xaxis_transform(which='grid')
        else:
            raise ValueError('unknown spine spine_type: %s' %
                             self.spine_type)

        if what == 'identity':
            return base_transform
        elif what == 'post':
            return base_transform + how
        elif what == 'pre':
            return how + base_transform
        else:
            raise ValueError("unknown spine_transform type: %s" % what)
