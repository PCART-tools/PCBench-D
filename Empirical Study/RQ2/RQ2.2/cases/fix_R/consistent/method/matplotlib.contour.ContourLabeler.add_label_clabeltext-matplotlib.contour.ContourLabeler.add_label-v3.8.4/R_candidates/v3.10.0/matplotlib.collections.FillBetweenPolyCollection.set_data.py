    def set_data(self, t, f1, f2, *, where=None):
        """
        Set new values for the two bounding curves.

        Parameters
        ----------
        t : array (length N)
            The ``self.t_direction`` coordinates of the nodes defining the curves.

        f1 : array (length N) or scalar
            The other coordinates of the nodes defining the first curve.

        f2 : array (length N) or scalar
            The other coordinates of the nodes defining the second curve.

        where : array of bool (length N), optional
            Define *where* to exclude some {dir} regions from being filled.
            The filled regions are defined by the coordinates ``t[where]``.
            More precisely, fill between ``t[i]`` and ``t[i+1]`` if
            ``where[i] and where[i+1]``.  Note that this definition implies
            that an isolated *True* value between two *False* values in *where*
            will not result in filling.  Both sides of the *True* position
            remain unfilled due to the adjacent *False* values.

        See Also
        --------
        .PolyCollection.set_verts, .Line2D.set_data
        """
        t, f1, f2 = self.axes._fill_between_process_units(
            self.t_direction, self._f_direction, t, f1, f2)

        verts = self._make_verts(t, f1, f2, where)
        self.set_verts(verts)
