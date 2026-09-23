    def contains_branch_seperately(self, other_transform):
        """
        Return whether the given branch is a sub-tree of this transform on
        each separate dimension.

        A common use for this method is to identify if a transform is a blended
        transform containing an Axes' data transform. e.g.::

            x_isdata, y_isdata = trans.contains_branch_seperately(ax.transData)

        """
        if self.output_dims != 2:
            raise ValueError('contains_branch_seperately only supports '
                             'transforms with 2 output dimensions')
        # for a non-blended transform each separate dimension is the same, so
        # just return the appropriate shape.
        return (self.contains_branch(other_transform), ) * 2
