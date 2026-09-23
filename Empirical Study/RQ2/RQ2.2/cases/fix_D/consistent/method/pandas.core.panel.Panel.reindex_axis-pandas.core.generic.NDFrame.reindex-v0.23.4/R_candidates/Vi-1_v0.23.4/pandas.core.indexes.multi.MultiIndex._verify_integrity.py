    def _verify_integrity(self, labels=None, levels=None):
        """

        Parameters
        ----------
        labels : optional list
            Labels to check for validity. Defaults to current labels.
        levels : optional list
            Levels to check for validity. Defaults to current levels.

        Raises
        ------
        ValueError
            If length of levels and labels don't match, if any label would
            exceed level bounds, or there are any duplicate levels.
        """
        # NOTE: Currently does not check, among other things, that cached
        # nlevels matches nor that sortorder matches actually sortorder.
        labels = labels or self.labels
        levels = levels or self.levels

        if len(levels) != len(labels):
            raise ValueError("Length of levels and labels must match. NOTE:"
                             " this index is in an inconsistent state.")
        label_length = len(self.labels[0])
        for i, (level, label) in enumerate(zip(levels, labels)):
            if len(label) != label_length:
                raise ValueError("Unequal label lengths: %s" %
                                 ([len(lab) for lab in labels]))
            if len(label) and label.max() >= len(level):
                raise ValueError("On level %d, label max (%d) >= length of"
                                 " level  (%d). NOTE: this index is in an"
                                 " inconsistent state" % (i, label.max(),
                                                          len(level)))
            if not level.is_unique:
                raise ValueError("Level values must be unique: {values} on "
                                 "level {level}".format(
                                     values=[value for value in level],
                                     level=i))
