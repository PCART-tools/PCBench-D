    def _update_patch_limits(self, patch):
        """update the data limits for patch *p*"""
        # hist can add zero height Rectangles, which is useful to keep
        # the bins, counts and patches lined up, but it throws off log
        # scaling.  We'll ignore rects with zero height or width in
        # the auto-scaling

        # cannot check for '==0' since unitized data may not compare to zero
        # issue #2150 - we update the limits if patch has non zero width
        # or height.
        if (isinstance(patch, mpatches.Rectangle) and
                ((not patch.get_width()) and (not patch.get_height()))):
            return
        vertices = patch.get_path().vertices
        if vertices.size > 0:
            xys = patch.get_patch_transform().transform(vertices)
            if patch.get_data_transform() != self.transData:
                patch_to_data = (patch.get_data_transform() -
                                 self.transData)
                xys = patch_to_data.transform(xys)

            updatex, updatey = patch.get_transform().\
                contains_branch_seperately(self.transData)
            self.update_datalim(xys, updatex=updatex,
                                updatey=updatey)
