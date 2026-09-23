    def expose(self, handle):
        """
        Copy the bitmap contents to a device context.

        :param handle: Device context (HDC), cast to a Python integer, or an
                       HDC or HWND instance.  In PythonWin, you can use
                       ``CDC.GetHandleAttrib()`` to get a suitable handle.
        """
        if isinstance(handle, HWND):
            dc = self.image.getdc(handle)
            try:
                result = self.image.expose(dc)
            finally:
                self.image.releasedc(handle, dc)
        else:
            result = self.image.expose(handle)
        return result
