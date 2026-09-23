    def labels(self, inline, inline_spacing):
        for idx, (icon, lev, cvalue) in enumerate(zip(
                self.labelIndiceList,
                self.labelLevelList,
                self.labelCValueList,
        )):
            trans = self.get_transform()
            label_width = self._get_nth_label_width(idx)
            additions = []
            for subpath in self._paths[icon]._iter_connected_components():
                screen_xys = trans.transform(subpath.vertices)
                # Check if long enough for a label
                if self.print_label(screen_xys, label_width):
                    x, y, idx = self.locate_label(screen_xys, label_width)
                    rotation, path = self._split_path_and_get_label_rotation(
                        subpath, idx, (x, y),
                        label_width, inline_spacing)
                    self.add_label(x, y, rotation, lev, cvalue)  # Really add label.
                    if inline:  # If inline, add new contours
                        additions.append(path)
                else:  # If not adding label, keep old path
                    additions.append(subpath)
            # After looping over all segments on a contour, replace old path by new one
            # if inlining.
            if inline:
                self._paths[icon] = Path.make_compound_path(*additions)
