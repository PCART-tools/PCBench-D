    def save(self, fp, format=None, **params):
        """
        Saves this image under the given filename.  If no format is
        specified, the format to use is determined from the filename
        extension, if possible.

        Keyword options can be used to provide additional instructions
        to the writer. If a writer doesn't recognise an option, it is
        silently ignored. The available options are described in the
        :doc:`image format documentation
        <../handbook/image-file-formats>` for each writer.

        You can use a file object instead of a filename. In this case,
        you must always specify the format. The file object must
        implement the ``seek``, ``tell``, and ``write``
        methods, and be opened in binary mode.

        :param fp: A filename (string), pathlib.Path object or file object.
        :param format: Optional format override.  If omitted, the
           format to use is determined from the filename extension.
           If a file object was used instead of a filename, this
           parameter should always be used.
        :param params: Extra parameters to the image writer.
        :returns: None
        :exception ValueError: If the output format could not be determined
           from the file name.  Use the format option to solve this.
        :exception OSError: If the file could not be written.  The file
           may have been created, and may contain partial data.
        """

        filename = ""
        open_fp = False
        if isinstance(fp, Path):
            filename = str(fp)
            open_fp = True
        elif is_path(fp):
            filename = fp
            open_fp = True
        elif fp == sys.stdout:
            try:
                fp = sys.stdout.buffer
            except AttributeError:
                pass
        if not filename and hasattr(fp, "name") and is_path(fp.name):
            # only set the name for metadata purposes
            filename = fp.name

        # may mutate self!
        self._ensure_mutable()

        save_all = params.pop("save_all", False)
        self.encoderinfo = params
        self.encoderconfig = ()

        preinit()

        ext = os.path.splitext(filename)[1].lower()

        if not format:
            if ext not in EXTENSION:
                init()
            try:
                format = EXTENSION[ext]
            except KeyError as e:
                msg = f"unknown file extension: {ext}"
                raise ValueError(msg) from e

        if format.upper() not in SAVE:
            init()
        if save_all:
            save_handler = SAVE_ALL[format.upper()]
        else:
            save_handler = SAVE[format.upper()]

        created = False
        if open_fp:
            created = not os.path.exists(filename)
            if params.get("append", False):
                # Open also for reading ("+"), because TIFF save_all
                # writer needs to go back and edit the written data.
                fp = builtins.open(filename, "r+b")
            else:
                fp = builtins.open(filename, "w+b")

        try:
            save_handler(self, fp, filename)
        except Exception:
            if open_fp:
                fp.close()
            if created:
                try:
                    os.remove(filename)
                except PermissionError:
                    pass
            raise
        if open_fp:
            fp.close()
