    def expose(self, handle: int | HDC | HWND) -> None:
        """
        Copy the bitmap contents to a device context.

        :param handle: Device context (HDC), cast to a Python integer, or an
                       HDC or HWND instance.  In PythonWin, you can use
                       ``CDC.GetHandleAttrib()`` to get a suitable handle.
        """
        handle_int = int(handle)
        if isinstance(handle, HWND):
            dc = self.image.getdc(handle_int)
            try:
                self.image.expose(dc)
            finally:
                self.image.releasedc(handle_int, dc)
        else:
            self.image.expose(handle_int)
