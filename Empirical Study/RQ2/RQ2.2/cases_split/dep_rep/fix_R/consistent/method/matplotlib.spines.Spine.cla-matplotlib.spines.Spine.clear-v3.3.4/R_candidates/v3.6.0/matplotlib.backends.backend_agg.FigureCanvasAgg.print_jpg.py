    @_api.delete_parameter("3.5", "args")
    def print_jpg(self, filename_or_obj, *args, pil_kwargs=None):
        # savefig() has already applied savefig.facecolor; we now set it to
        # white to make imsave() blend semi-transparent figures against an
        # assumed white background.
        with mpl.rc_context({"savefig.facecolor": "white"}):
            self._print_pil(filename_or_obj, "jpeg", pil_kwargs)
