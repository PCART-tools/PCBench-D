    def __getstate__(self):
        block_values = [b.values for b in self.blocks]
        block_items = [b.items for b in self.blocks]
        axes_array = [ax for ax in self.axes]
        return axes_array, block_values, block_items
