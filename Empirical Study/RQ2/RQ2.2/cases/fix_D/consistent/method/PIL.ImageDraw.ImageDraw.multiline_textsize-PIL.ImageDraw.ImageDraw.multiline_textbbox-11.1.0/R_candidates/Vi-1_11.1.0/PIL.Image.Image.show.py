    def show(self, title: str | None = None) -> None:
        """
        Displays this image. This method is mainly intended for debugging purposes.

        This method calls :py:func:`PIL.ImageShow.show` internally. You can use
        :py:func:`PIL.ImageShow.register` to override its default behaviour.

        The image is first saved to a temporary file. By default, it will be in
        PNG format.

        On Unix, the image is then opened using the **xdg-open**, **display**,
        **gm**, **eog** or **xv** utility, depending on which one can be found.

        On macOS, the image is opened with the native Preview application.

        On Windows, the image is opened with the standard PNG display utility.

        :param title: Optional title to use for the image window, where possible.
        """

        _show(self, title=title)
