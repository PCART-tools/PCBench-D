    def get_transform(self):
        """
        Return the :class:`~matplotlib.transforms.Transform`
        instance used by this ContourSet.
        """
        if self._transform is None:
            self._transform = self.axes.transData
        elif (not isinstance(self._transform, mtransforms.Transform)
              and hasattr(self._transform, '_as_mpl_transform')):
            self._transform = self._transform._as_mpl_transform(self.axes)
        return self._transform
