    def _update_offset_text_position(self, bboxes, bboxes2):
        """
        Update the offset text position based on the sequence of bounding
        boxes of all the ticklabels.
        """
        raise NotImplementedError('Derived must override')
