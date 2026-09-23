    def stop_filter(self, filter_func):
        """
        Used in AggRenderer. Switch back to the original renderer.
        The contents of the temporary renderer is processed with the
        *filter_func* and is drawn on the original renderer as an
        image.
        """
