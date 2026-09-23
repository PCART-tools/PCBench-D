    def get_datalim(self, transData):
        """Calculate the data limits and return them as a `.Bbox`."""
        datalim = transforms.Bbox.null()
        datalim.update_from_data_xy((self.get_transform() - transData).transform(
            np.concatenate([self._bbox, [self._bbox.minpos]])))
        return datalim
