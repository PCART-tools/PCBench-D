    def _get_compressed_triangulation(self, return_tri_renum=False,
                                      return_node_renum=False):
        """
        Compress (if masked) the encapsulated triangulation.

        Returns minimal-length triangles array (*compressed_triangles*) and
        coordinates arrays (*compressed_x*, *compressed_y*) that can still
        describe the unmasked triangles of the encapsulated triangulation.

        Parameters
        ----------
        return_tri_renum : boolean, optional
            Indicates whether a renumbering table to translate the triangle
            numbers from the encapsulated triangulation numbering into the
            new (compressed) renumbering will be returned.
        return_node_renum : boolean, optional
            Indicates whether a renumbering table to translate the nodes
            numbers from the encapsulated triangulation numbering into the
            new (compressed) renumbering will be returned.

        Returns
        -------
        compressed_triangles : array-like
            the returned compressed triangulation triangles
        compressed_x : array-like
            the returned compressed triangulation 1st coordinate
        compressed_y : array-like
            the returned compressed triangulation 2nd coordinate
        tri_renum : array-like of integers
            renumbering table to translate the triangle numbers from the
            encapsulated triangulation into the new (compressed) renumbering.
            -1 for masked triangles (deleted from *compressed_triangles*).
            Returned only if *return_tri_renum* is True.
        node_renum : array-like of integers
            renumbering table to translate the point numbers from the
            encapsulated triangulation into the new (compressed) renumbering.
            -1 for unused points (i.e. those deleted from *compressed_x* and
            *compressed_y*). Returned only if *return_node_renum* is True.

        """
        # Valid triangles and renumbering
        tri_mask = self._triangulation.mask
        compressed_triangles = self._triangulation.get_masked_triangles()
        ntri = self._triangulation.triangles.shape[0]
        tri_renum = self._total_to_compress_renum(tri_mask, ntri)

        # Valid nodes and renumbering
        node_mask = (np.bincount(np.ravel(compressed_triangles),
                                 minlength=self._triangulation.x.size) == 0)
        compressed_x = self._triangulation.x[~node_mask]
        compressed_y = self._triangulation.y[~node_mask]
        node_renum = self._total_to_compress_renum(node_mask)

        # Now renumbering the valid triangles nodes
        compressed_triangles = node_renum[compressed_triangles]

        # 4 cases possible for return
        if not return_tri_renum:
            if not return_node_renum:
                return compressed_triangles, compressed_x, compressed_y
            else:
                return (compressed_triangles, compressed_x, compressed_y,
                        node_renum)
        else:
            if not return_node_renum:
                return (compressed_triangles, compressed_x, compressed_y,
                        tri_renum)
            else:
                return (compressed_triangles, compressed_x, compressed_y,
                        tri_renum, node_renum)
