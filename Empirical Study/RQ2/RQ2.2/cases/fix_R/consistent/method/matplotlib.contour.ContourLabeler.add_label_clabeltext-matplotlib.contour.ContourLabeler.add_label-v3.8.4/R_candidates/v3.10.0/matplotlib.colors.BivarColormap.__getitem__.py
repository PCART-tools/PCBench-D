    def __getitem__(self, item):
        """Creates and returns a colorbar along the selected axis"""
        if not self._isinit:
            self._init()
        if item == 0:
            origin_1_as_int = int(self._origin[1]*self.M)
            if origin_1_as_int > self.M-1:
                origin_1_as_int = self.M-1
            one_d_lut = self._lut[:, origin_1_as_int]
            new_cmap = ListedColormap(one_d_lut, name=f'{self.name}_0', N=self.N)

        elif item == 1:
            origin_0_as_int = int(self._origin[0]*self.N)
            if origin_0_as_int > self.N-1:
                origin_0_as_int = self.N-1
            one_d_lut = self._lut[origin_0_as_int, :]
            new_cmap = ListedColormap(one_d_lut, name=f'{self.name}_1', N=self.M)
        else:
            raise KeyError(f"only 0 or 1 are"
                           f" valid keys for BivarColormap, not {item!r}")
        new_cmap._rgba_bad = self._rgba_bad
        if self.shape in ['ignore', 'circleignore']:
            new_cmap.set_over(self._rgba_outside)
            new_cmap.set_under(self._rgba_outside)
        return new_cmap
