    def refine_triangulation(self, return_tri_index=False, subdiv=3):
        """
        Computes an uniformly refined triangulation *refi_triangulation* of
        the encapsulated :attr:`triangulation`.

        This function refines the encapsulated triangulation by splitting each
        father triangle into 4 child sub-triangles built on the edges midside
        nodes, recursively (level of recursion *subdiv*).
        In the end, each triangle is hence divided into ``4**subdiv``
        child triangles.
        The default value for *subdiv* is 3 resulting in 64 refined
        subtriangles for each triangle of the initial triangulation.

        Parameters
        ----------
        return_tri_index : boolean, optional
            Boolean indicating whether an index table indicating the father
            triangle index of each point will be returned. Default value
            False.
        subdiv : integer, optional
            Recursion level for the subdivision. Defaults value 3.
            Each triangle will be divided into ``4**subdiv`` child triangles.

        Returns
        -------
        refi_triangulation : :class:`~matplotlib.tri.Triangulation`
            The returned refined triangulation
        found_index : array-like of integers
            Index of the initial triangulation containing triangle, for each
            point of *refi_triangulation*.
            Returned only if *return_tri_index* is set to True.

        """
        refi_triangulation = self._triangulation
        ntri = refi_triangulation.triangles.shape[0]

        # Computes the triangulation ancestors numbers in the reference
        # triangulation.
        ancestors = np.arange(ntri, dtype=np.int32)
        for _ in range(subdiv):
            refi_triangulation, ancestors = self._refine_triangulation_once(
                refi_triangulation, ancestors)
        refi_npts = refi_triangulation.x.shape[0]
        refi_triangles = refi_triangulation.triangles

        # Now we compute found_index table if needed
        if return_tri_index:
            # We have to initialize found_index with -1 because some nodes
            # may very well belong to no triangle at all, e.g., in case of
            # Delaunay Triangulation with DuplicatePointWarning.
            found_index = - np.ones(refi_npts, dtype=np.int32)
            tri_mask = self._triangulation.mask
            if tri_mask is None:
                found_index[refi_triangles] = np.repeat(ancestors,
                                                        3).reshape(-1, 3)
            else:
                # There is a subtlety here: we want to avoid whenever possible
                # that refined points container is a masked triangle (which
                # would result in artifacts in plots).
                # So we impose the numbering from masked ancestors first,
                # then overwrite it with unmasked ancestor numbers.
                ancestor_mask = tri_mask[ancestors]
                found_index[refi_triangles[ancestor_mask, :]
                            ] = np.repeat(ancestors[ancestor_mask],
                                          3).reshape(-1, 3)
                found_index[refi_triangles[~ancestor_mask, :]
                            ] = np.repeat(ancestors[~ancestor_mask],
                                          3).reshape(-1, 3)
            return refi_triangulation, found_index
        else:
            return refi_triangulation
