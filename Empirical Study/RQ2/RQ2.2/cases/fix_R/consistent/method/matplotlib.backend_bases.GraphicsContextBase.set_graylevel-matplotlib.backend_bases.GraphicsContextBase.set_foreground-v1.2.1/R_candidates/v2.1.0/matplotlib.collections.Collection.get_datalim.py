    def get_datalim(self, transData):
        transform = self.get_transform()
        transOffset = self.get_offset_transform()
        offsets = self._offsets
        paths = self.get_paths()

        if not transform.is_affine:
            paths = [transform.transform_path_non_affine(p) for p in paths]
            transform = transform.get_affine()
        if not transOffset.is_affine:
            offsets = transOffset.transform_non_affine(offsets)
            transOffset = transOffset.get_affine()

        if isinstance(offsets, np.ma.MaskedArray):
            offsets = offsets.filled(np.nan)
            # get_path_collection_extents handles nan but not masked arrays

        if len(paths) and len(offsets):
            result = mpath.get_path_collection_extents(
                transform.frozen(), paths, self.get_transforms(),
                offsets, transOffset.frozen())
            result = result.inverse_transformed(transData)
        else:
            result = transforms.Bbox.null()
        return result
