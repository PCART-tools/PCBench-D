    def draw_path_collection(self, gc, master_transform, paths, all_transforms,
                             offsets, offsetTrans, facecolors, edgecolors,
                             linewidths, linestyles, antialiaseds, urls,
                             offset_position):
        if offset_position == "data":
            cbook.warn_deprecated(
                "3.3", message="Support for offset_position='data' is "
                "deprecated since %(since)s and will be removed %(removal)s.")
        return self._renderer.draw_path_collection(
            gc, master_transform, paths, all_transforms, offsets, offsetTrans,
            facecolors, edgecolors, linewidths, linestyles, antialiaseds, urls,
            offset_position)
