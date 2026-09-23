    def _repr_image(self, image_format, **kwargs):
        """Helper function for iPython display hook.

        :param image_format: Image format.
        :returns: image as bytes, saved into the given format.
        """
        b = io.BytesIO()
        try:
            self.save(b, image_format, **kwargs)
        except Exception:
            return None
        return b.getvalue()
