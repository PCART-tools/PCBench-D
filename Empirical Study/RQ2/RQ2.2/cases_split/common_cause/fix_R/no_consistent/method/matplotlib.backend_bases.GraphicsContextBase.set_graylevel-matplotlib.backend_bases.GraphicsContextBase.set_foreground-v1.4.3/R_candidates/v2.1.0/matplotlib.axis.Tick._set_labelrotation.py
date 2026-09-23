    def _set_labelrotation(self, labelrotation):
        if isinstance(labelrotation, six.string_types):
            mode = labelrotation
            angle = 0
        elif isinstance(labelrotation, (tuple, list)):
            mode, angle = labelrotation
        else:
            mode = 'default'
            angle = labelrotation
        if mode not in ('auto', 'default'):
            raise ValueError("Label rotation mode must be 'default' or "
                             "'auto', not '{}'.".format(mode))
        self._labelrotation = (mode, angle)
