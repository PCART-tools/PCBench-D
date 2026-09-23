class _SVGConverter(_Converter):
    def __call__(self, orig, dest):
        old_inkscape = mpl._get_executable_info("inkscape").version < "1"
        terminator = b"\n>" if old_inkscape else b"> "
        if not hasattr(self, "_tmpdir"):
            self._tmpdir = TemporaryDirectory()
            # On Windows, we must make sure that self._proc has terminated
            # (which __del__ does) before clearing _tmpdir.
            weakref.finalize(self._tmpdir, self.__del__)
        if (not self._proc  # First run.
                or self._proc.poll() is not None):  # Inkscape terminated.
            env = {
                **os.environ,
                # If one passes e.g. a png file to Inkscape, it will try to
                # query the user for conversion options via a GUI (even with
                # `--without-gui`).  Unsetting `DISPLAY` prevents this (and
                # causes GTK to crash and Inkscape to terminate, but that'll
                # just be reported as a regular exception below).
                "DISPLAY": "",
                # Do not load any user options.
                "INKSCAPE_PROFILE_DIR": os.devnull,
            }
            # Old versions of Inkscape (e.g. 0.48.3.1) seem to sometimes
            # deadlock when stderr is redirected to a pipe, so we redirect it
            # to a temporary file instead.  This is not necessary anymore as of
            # Inkscape 0.92.1.
            stderr = TemporaryFile()
            self._proc = subprocess.Popen(
                ["inkscape", "--without-gui", "--shell"] if old_inkscape else
                ["inkscape", "--shell"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
                env=env, cwd=self._tmpdir.name)
            # Slight abuse, but makes shutdown handling easier.
            self._proc.stderr = stderr
            try:
                self._read_until(terminator)
            except _ConverterError as err:
                raise OSError("Failed to start Inkscape in interactive "
                              "mode") from err

        # Inkscape's shell mode does not support escaping metacharacters in the
        # filename ("\n", and ":;" for inkscape>=1).  Avoid any problems by
        # running from a temporary directory and using fixed filenames.
        inkscape_orig = Path(self._tmpdir.name, os.fsdecode(b"f.svg"))
        inkscape_dest = Path(self._tmpdir.name, os.fsdecode(b"f.png"))
        try:
            inkscape_orig.symlink_to(Path(orig).resolve())
        except OSError:
            shutil.copyfile(orig, inkscape_orig)
        self._proc.stdin.write(
            b"f.svg --export-png=f.png\n" if old_inkscape else
            b"file-open:f.svg;export-filename:f.png;export-do;file-close\n")
        self._proc.stdin.flush()
        try:
            self._read_until(terminator)
        except _ConverterError as err:
            # Inkscape's output is not localized but gtk's is, so the output
            # stream probably has a mixed encoding.  Using the filesystem
            # encoding should at least get the filenames right...
            self._proc.stderr.seek(0)
            raise ImageComparisonFailure(
                self._proc.stderr.read().decode(
                    sys.getfilesystemencoding(), "replace")) from err
        os.remove(inkscape_orig)
        shutil.move(inkscape_dest, dest)

    def __del__(self):
        super().__del__()
        if hasattr(self, "_tmpdir"):
            self._tmpdir.cleanup()
