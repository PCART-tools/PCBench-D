    def _compute_dof(self, kind, dz=None):
        """
        Computes and returns nodal dofs according to kind

        Parameters
        ----------
        kind : {'min_E', 'geom', 'user'}
            Choice of the _DOF_estimator subclass to perform the gradient
            estimation.
        dz : tuple of array_likes (dzdx, dzdy), optional
            Used only if *kind*=user; in this case passed to the
            :class:`_DOF_estimator_user`.

        Returns
        -------
        dof : array_like, shape (npts,2)
              Estimation of the gradient at triangulation nodes (stored as
              degree of freedoms of reduced-HCT triangle elements).
        """
        if kind == 'user':
            if dz is None:
                raise ValueError("For a CubicTriInterpolator with "
                                 "*kind*='user', a valid *dz* "
                                 "argument is expected.")
            TE = _DOF_estimator_user(self, dz=dz)
        elif kind == 'geom':
            TE = _DOF_estimator_geom(self)
        elif kind == 'min_E':
            TE = _DOF_estimator_min_E(self)
        else:
            raise ValueError("CubicTriInterpolator *kind* proposed: {0}; "
                             "should be one of: "
                             "'user', 'geom', 'min_E'".format(kind))
        return TE.compute_dof_from_df()
