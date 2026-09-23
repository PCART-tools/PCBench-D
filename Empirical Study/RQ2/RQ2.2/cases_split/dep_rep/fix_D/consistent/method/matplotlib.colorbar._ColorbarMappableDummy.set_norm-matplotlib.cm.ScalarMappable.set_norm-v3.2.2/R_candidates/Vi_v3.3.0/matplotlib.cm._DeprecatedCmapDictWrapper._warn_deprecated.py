    def _warn_deprecated(self):
        cbook.warn_deprecated(
            "3.3",
            message="The global colormaps dictionary is no longer "
                    "considered public API.",
            alternative="Please use register_cmap() and get_cmap() to "
                        "access the contents of the dictionary."
        )
