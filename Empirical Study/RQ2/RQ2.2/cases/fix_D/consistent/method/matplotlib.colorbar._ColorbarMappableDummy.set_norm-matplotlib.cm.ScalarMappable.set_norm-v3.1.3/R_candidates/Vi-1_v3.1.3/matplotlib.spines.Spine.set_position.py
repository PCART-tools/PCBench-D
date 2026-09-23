    def set_position(self, position):
        """Set the position of the spine.

        Spine position is specified by a 2 tuple of (position type,
        amount). The position types are:

        * 'outward' : place the spine out from the data area by the
          specified number of points. (Negative values specify placing the
          spine inward.)

        * 'axes' : place the spine at the specified Axes coordinate (from
          0.0-1.0).

        * 'data' : place the spine at the specified data coordinate.

        Additionally, shorthand notations define a special positions:

        * 'center' -> ('axes',0.5)
        * 'zero' -> ('data', 0.0)

        """
        if position in ('center', 'zero'):
            # special positions
            pass
        else:
            if len(position) != 2:
                raise ValueError("position should be 'center' or 2-tuple")
            if position[0] not in ['outward', 'axes', 'data']:
                raise ValueError("position[0] should be one of 'outward', "
                                 "'axes', or 'data' ")
        self._position = position
        self._calc_offset_transform()

        self.set_transform(self.get_spine_transform())

        if self.axis is not None:
            self.axis.reset_ticks()
        self.stale = True
