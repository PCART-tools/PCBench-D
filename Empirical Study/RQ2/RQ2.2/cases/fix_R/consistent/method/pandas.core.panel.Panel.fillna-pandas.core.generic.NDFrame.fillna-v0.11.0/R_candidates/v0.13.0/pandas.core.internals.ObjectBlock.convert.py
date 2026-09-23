    def convert(self, convert_dates=True, convert_numeric=True, copy=True,
                by_item=True):
        """ attempt to coerce any object types to better types
            return a copy of the block (if copy = True)
            by definition we ARE an ObjectBlock!!!!!

            can return multiple blocks!
            """

        # attempt to create new type blocks
        is_unique = self.items.is_unique
        blocks = []
        if by_item and not self._is_single_block:

            for i, c in enumerate(self.items):
                values = self.iget(i)

                values = com._possibly_convert_objects(
                    values.ravel(), convert_dates=convert_dates,
                    convert_numeric=convert_numeric
                ).reshape(values.shape)
                values = _block_shape(values, ndim=self.ndim)
                items = self.items.take([i])
                placement = None if is_unique else [i]
                newb = make_block(values, items, self.ref_items,
                                  ndim=self.ndim, placement=placement)
                blocks.append(newb)

        else:

            values = com._possibly_convert_objects(
                self.values.ravel(), convert_dates=convert_dates,
                convert_numeric=convert_numeric
            ).reshape(self.values.shape)
            blocks.append(make_block(values, self.items, self.ref_items,
                                     ndim=self.ndim))

        return blocks
