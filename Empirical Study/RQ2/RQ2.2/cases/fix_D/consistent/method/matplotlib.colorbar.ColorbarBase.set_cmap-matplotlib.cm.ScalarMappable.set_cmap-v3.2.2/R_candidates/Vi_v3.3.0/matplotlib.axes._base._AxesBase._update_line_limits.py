    def _update_line_limits(self, line):
        """
        Figures out the data limit of the given line, updating self.dataLim.
        """
        path = line.get_path()
        if path.vertices.size == 0:
            return

        line_trans = line.get_transform()

        if line_trans == self.transData:
            data_path = path

        elif any(line_trans.contains_branch_seperately(self.transData)):
            # identify the transform to go from line's coordinates
            # to data coordinates
            trans_to_data = line_trans - self.transData

            # if transData is affine we can use the cached non-affine component
            # of line's path. (since the non-affine part of line_trans is
            # entirely encapsulated in trans_to_data).
            if self.transData.is_affine:
                line_trans_path = line._get_transformed_path()
                na_path, _ = line_trans_path.get_transformed_path_and_affine()
                data_path = trans_to_data.transform_path_affine(na_path)
            else:
                data_path = trans_to_data.transform_path(path)
        else:
            # for backwards compatibility we update the dataLim with the
            # coordinate range of the given path, even though the coordinate
            # systems are completely different. This may occur in situations
            # such as when ax.transAxes is passed through for absolute
            # positioning.
            data_path = path

        if data_path.vertices.size > 0:
            updatex, updatey = line_trans.contains_branch_seperately(
                self.transData)
            self.dataLim.update_from_path(data_path,
                                          self.ignore_existing_data_limits,
                                          updatex=updatex,
                                          updatey=updatey)
            self.ignore_existing_data_limits = False
