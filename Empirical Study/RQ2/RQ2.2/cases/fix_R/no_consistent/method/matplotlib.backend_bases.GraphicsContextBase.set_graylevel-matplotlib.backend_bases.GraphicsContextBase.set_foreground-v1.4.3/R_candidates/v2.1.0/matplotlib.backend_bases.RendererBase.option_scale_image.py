    def option_scale_image(self):
        """
        override this method for renderers that support arbitrary affine
        transformations in :meth:`draw_image` (most vector backends).
        """
        return False
