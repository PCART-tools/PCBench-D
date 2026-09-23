    def _verify_integrity(self):
        """Raises ValueError if length of levels and labels don't match or any
        label would exceed level bounds"""
        # NOTE: Currently does not check, among other things, that cached
        # nlevels matches nor that sortorder matches actually sortorder.
        labels, levels = self.labels, self.levels
        if len(levels) != len(labels):
            raise ValueError("Length of levels and labels must match. NOTE:"
                             " this index is in an inconsistent state.")
        label_length = len(self.labels[0])
        for i, (level, label) in enumerate(zip(levels, labels)):
            if len(label) != label_length:
                raise ValueError("Unequal label lengths: %s" % (
                                 [len(lab) for lab in labels]))
            if len(label) and label.max() >= len(level):
                raise ValueError("On level %d, label max (%d) >= length of"
                                 " level  (%d). NOTE: this index is in an"
                                 " inconsistent state" % (i, label.max(),
                                                          len(level)))
