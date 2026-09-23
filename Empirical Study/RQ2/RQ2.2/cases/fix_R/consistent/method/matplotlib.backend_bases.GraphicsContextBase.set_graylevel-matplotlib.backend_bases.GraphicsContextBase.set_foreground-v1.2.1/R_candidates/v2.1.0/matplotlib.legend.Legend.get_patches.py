    def get_patches(self):
        'return a list of patch instances in the legend'
        return silent_list('Patch',
                           [h for h in self.legendHandles
                            if isinstance(h, Patch)])
