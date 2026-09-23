    def get_transform(self):
        """
        Return the :class:`~matplotlib.transforms.Transform` applied
        to the children
        """
        return self.aux_transform + \
               self.ref_offset_transform + \
               self.offset_transform
