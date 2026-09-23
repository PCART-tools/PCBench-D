    def _concat_blocks(self, blocks, values):
        """
        validate that we can merge these blocks

        return the block concatenation
        """

        categories = self.values.categories
        for b in blocks:
            if not categories.equals(b.values.categories):
                raise ValueError("incompatible levels in categorical block merge")

        return self._holder(values[0], categories=categories)
