    def __call__(self, orig, dest):
        if (not self._proc  # First run.
                or self._proc.poll() is not None):  # Inkscape terminated.
            env = os.environ.copy()
            # If one passes e.g. a png file to Inkscape, it will try to
            # query the user for conversion options via a GUI (even with
            # `--without-gui`).  Unsetting `DISPLAY` prevents this (and causes
            # GTK to crash and Inkscape to terminate, but that'll just be
            # reported as a regular exception below).
            env.pop("DISPLAY", None)  # May already be unset.
            # Do not load any user options.
            # `os.environ` needs native strings on Py2+Windows.
            env[str("INKSCAPE_PROFILE_DIR")] = os.devnull
            # Old versions of Inkscape (0.48.3.1, used on Travis as of now)
            # seem to sometimes deadlock when stderr is redirected to a pipe,
            # so we redirect it to a temporary file instead.  This is not
            # necessary anymore as of Inkscape 0.92.1.
            self._stderr = TemporaryFile()
            self._proc = subprocess.Popen(
                [str("inkscape"), "--without-gui", "--shell"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=self._stderr, env=env)
            if not self._read_to_prompt():
                raise OSError("Failed to start Inkscape")

        try:
            fsencode = os.fsencode
        except AttributeError:  # Py2.
            def fsencode(s):
                return s.encode(sys.getfilesystemencoding())

        # Inkscape uses glib's `g_shell_parse_argv`, which has a consistent
        # behavior across platforms, so we can just use `shlex.quote`.
        orig_b, dest_b = map(_shlex_quote_bytes, map(fsencode, [orig, dest]))
        if b"\n" in orig_b or b"\n" in dest_b:
            # Who knows whether the current folder name has a newline, or if
            # our encoding is even ASCII compatible...  Just fall back on the
            # slow solution (Inkscape uses `fgets` so it will always stop at a
            # newline).
            return make_external_conversion_command(lambda old, new: [
                str('inkscape'), '-z', old, '--export-png', new])(orig, dest)
        self._proc.stdin.write(orig_b + b" --export-png=" + dest_b + b"\n")
        self._proc.stdin.flush()
        if not self._read_to_prompt():
            # Inkscape's output is not localized but gtk's is, so the
            # output stream probably has a mixed encoding.  Using
            # `getfilesystemencoding` should at least get the filenames
            # right...
            self._stderr.seek(0)
            raise ImageComparisonFailure(
                self._stderr.read().decode(
                    sys.getfilesystemencoding(), "replace"))
