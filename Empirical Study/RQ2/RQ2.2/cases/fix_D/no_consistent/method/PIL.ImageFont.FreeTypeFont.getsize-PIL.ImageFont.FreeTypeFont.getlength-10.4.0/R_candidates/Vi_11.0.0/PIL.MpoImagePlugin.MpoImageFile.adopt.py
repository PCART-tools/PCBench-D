    @staticmethod
    def adopt(
        jpeg_instance: JpegImagePlugin.JpegImageFile,
        mpheader: dict[int, Any] | None = None,
    ) -> MpoImageFile:
        """
        Transform the instance of JpegImageFile into
        an instance of MpoImageFile.
        After the call, the JpegImageFile is extended
        to be an MpoImageFile.

        This is essentially useful when opening a JPEG
        file that reveals itself as an MPO, to avoid
        double call to _open.
        """
        jpeg_instance.__class__ = MpoImageFile
        mpo_instance = cast(MpoImageFile, jpeg_instance)
        mpo_instance._after_jpeg_open(mpheader)
        return mpo_instance
