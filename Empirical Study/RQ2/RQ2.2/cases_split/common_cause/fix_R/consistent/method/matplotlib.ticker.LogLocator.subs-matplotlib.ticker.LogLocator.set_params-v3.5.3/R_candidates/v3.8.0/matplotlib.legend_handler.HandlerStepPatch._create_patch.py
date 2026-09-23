    @staticmethod
    def _create_patch(orig_handle, xdescent, ydescent, width, height):
        return Rectangle(xy=(-xdescent, -ydescent), width=width,
                         height=height, color=orig_handle.get_facecolor())
