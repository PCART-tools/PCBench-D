    def get_datalim(self, transData):
        # Calculate the data limits and return them as a `.Bbox`.
        #
        # This operation depends on the transforms for the data in the
        # collection and whether the collection has offsets:
        #
        # 1. offsets = None, transform child of transData: use the paths for
        # the automatic limits (i.e. for LineCollection in streamline).
        # 2. offsets != None: offset_transform is child of transData:
        #
        #    a. transform is child of transData: use the path + offset for
        #       limits (i.e for bar).
        #    b. transform is not a child of transData: just use the offsets
        #       for the limits (i.e. for scatter)
        #
        # 3. otherwise return a null Bbox.

        transform = self.get_transform()
        transOffset = self.get_offset_transform()
        hasOffsets = np.any(self._offsets)  # True if any non-zero offsets
        if hasOffsets and not transOffset.contains_branch(transData):
            # if there are offsets but in some coords other than data,
            # then don't use them for autoscaling.
            return transforms.Bbox.null()
        offsets = self._offsets

        paths = self.get_paths()

        if not transform.is_affine:
            paths = [transform.transform_path_non_affine(p) for p in paths]
            # Don't convert transform to transform.get_affine() here because
            # we may have transform.contains_branch(transData) but not
            # transforms.get_affine().contains_branch(transData).  But later,
            # be careful to only apply the affine part that remains.

        if isinstance(offsets, np.ma.MaskedArray):
            offsets = offsets.filled(np.nan)
            # get_path_collection_extents handles nan but not masked arrays

        if len(paths) and len(offsets):
            if any(transform.contains_branch_seperately(transData)):
                # collections that are just in data units (like quiver)
                # can properly have the axes limits set by their shape +
                # offset.  LineCollections that have no offsets can
                # also use this algorithm (like streamplot).
                return mpath.get_path_collection_extents(
                    transform.get_affine() - transData, paths,
                    self.get_transforms(),
                    transOffset.transform_non_affine(offsets),
                    transOffset.get_affine().frozen())
            if hasOffsets:
                # this is for collections that have their paths (shapes)
                # in physical, axes-relative, or figure-relative units
                # (i.e. like scatter). We can't uniquely set limits based on
                # those shapes, so we just set the limits based on their
                # location.

                offsets = (transOffset - transData).transform(offsets)
                # note A-B means A B^{-1}
                offsets = np.ma.masked_invalid(offsets)
                if not offsets.mask.all():
                    bbox = transforms.Bbox.null()
                    bbox.update_from_data_xy(offsets)
                    return bbox
        return transforms.Bbox.null()
