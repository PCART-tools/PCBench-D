    def close(self) -> None:
        """
        This operation will destroy the image core and release its memory.
        The image data will be unusable afterward.

        This function is required to close images that have multiple frames or
        have not had their file read and closed by the
        :py:meth:`~PIL.Image.Image.load` method. See :ref:`file-handling` for
        more information.
        """
        if getattr(self, "map", None):
            if sys.platform == "win32" and hasattr(sys, "pypy_version_info"):
                self.map.close()
            self.map: mmap.mmap | None = None

        # Instead of simply setting to None, we're setting up a
        # deferred error that will better explain that the core image
        # object is gone.
        self._im = DeferredError(ValueError("Operation on closed image"))
