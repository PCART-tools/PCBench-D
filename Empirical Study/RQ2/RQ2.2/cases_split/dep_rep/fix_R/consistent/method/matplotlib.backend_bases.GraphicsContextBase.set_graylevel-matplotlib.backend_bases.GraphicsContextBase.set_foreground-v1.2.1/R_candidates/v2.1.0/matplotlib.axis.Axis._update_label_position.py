    def _update_label_position(self, bboxes, bboxes2):
        """
        Update the label position based on the bounding box enclosing
        all the ticklabels and axis spine
        """
        raise NotImplementedError('Derived must override')
