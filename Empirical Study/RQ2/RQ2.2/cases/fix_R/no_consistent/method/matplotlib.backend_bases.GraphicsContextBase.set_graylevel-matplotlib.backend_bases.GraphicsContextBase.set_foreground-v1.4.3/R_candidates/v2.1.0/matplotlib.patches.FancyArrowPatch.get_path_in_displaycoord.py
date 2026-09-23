    def get_path_in_displaycoord(self):
        """
        Return the mutated path of the arrow in display coordinates.
        """

        dpi_cor = self.get_dpi_cor()

        if self._posA_posB is not None:
            posA = self.get_transform().transform_point(self._posA_posB[0])
            posB = self.get_transform().transform_point(self._posA_posB[1])
            _path = self.get_connectionstyle()(posA, posB,
                                               patchA=self.patchA,
                                               patchB=self.patchB,
                                               shrinkA=self.shrinkA * dpi_cor,
                                               shrinkB=self.shrinkB * dpi_cor
                                               )
        else:
            _path = self.get_transform().transform_path(self._path_original)

        _path, fillable = self.get_arrowstyle()(
            _path,
            self.get_mutation_scale() * dpi_cor,
            self.get_linewidth() * dpi_cor,
            self.get_mutation_aspect())

        # if not fillable:
        #    self._fill = False

        return _path, fillable
