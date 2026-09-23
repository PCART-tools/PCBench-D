    def get_patches(self):
        'Return a list of `~.patches.Patch` instances in the legend.'
        return silent_list('Patch',
                           [h for h in self.legendHandles
                            if isinstance(h, Patch)])
