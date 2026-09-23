    def get_checked_labels(self):
        """Return a list of labels currently checked by user."""

        return [l.get_text() for l, box_checked in
                zip(self.labels, self.get_status())
                if box_checked]
