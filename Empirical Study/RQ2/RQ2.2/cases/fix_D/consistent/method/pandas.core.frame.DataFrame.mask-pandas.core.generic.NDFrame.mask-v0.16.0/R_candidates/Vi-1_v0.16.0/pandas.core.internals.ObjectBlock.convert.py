    def convert(self, convert_dates=True, convert_numeric=True, convert_timedeltas=True,
                copy=True, by_item=True):
        """ attempt to coerce any object types to better types
            return a copy of the block (if copy = True)
            by definition we ARE an ObjectBlock!!!!!

            can return multiple blocks!
            """

        # attempt to create new type blocks
        blocks = []
        if by_item and not self._is_single_block:

            for i, rl in enumerate(self.mgr_locs):
                values = self.iget(i)

                values = com._possibly_convert_objects(
                    values.ravel(), convert_dates=convert_dates,
                    convert_numeric=convert_numeric,
                    convert_timedeltas=convert_timedeltas,
                ).reshape(values.shape)
                values = _block_shape(values, ndim=self.ndim)
                newb = make_block(values,
                                  ndim=self.ndim, placement=[rl])
                blocks.append(newb)

        else:

            values = com._possibly_convert_objects(
                self.values.ravel(), convert_dates=convert_dates,
                convert_numeric=convert_numeric
            ).reshape(self.values.shape)
            blocks.append(make_block(values,
                                     ndim=self.ndim, placement=self.mgr_locs))

        return blocks
