@writers.register('html')
class HTMLWriter(FileMovieWriter):
    """Writer for JavaScript-based HTML movies."""

    supported_formats = ['png', 'jpeg', 'tiff', 'svg']
    args_key = _api.deprecated("3.3")(property(
        lambda self: 'animation.html_args'))

    @classmethod
    def isAvailable(cls):
        return True

    def __init__(self, fps=30, codec=None, bitrate=None, extra_args=None,
                 metadata=None, embed_frames=False, default_mode='loop',
                 embed_limit=None):

        if extra_args:
            _log.warning("HTMLWriter ignores 'extra_args'")
        extra_args = ()  # Don't lookup nonexistent rcParam[args_key].
        self.embed_frames = embed_frames
        self.default_mode = default_mode.lower()
        _api.check_in_list(['loop', 'once', 'reflect'],
                           default_mode=self.default_mode)

        # Save embed limit, which is given in MB
        if embed_limit is None:
            self._bytes_limit = mpl.rcParams['animation.embed_limit']
        else:
            self._bytes_limit = embed_limit
        # Convert from MB to bytes
        self._bytes_limit *= 1024 * 1024

        super().__init__(fps, codec, bitrate, extra_args, metadata)

    def setup(self, fig, outfile, dpi, frame_dir=None):
        outfile = Path(outfile)
        _api.check_in_list(['.html', '.htm'], outfile_extension=outfile.suffix)

        self._saved_frames = []
        self._total_bytes = 0
        self._hit_limit = False

        if not self.embed_frames:
            if frame_dir is None:
                frame_dir = outfile.with_name(outfile.stem + '_frames')
            frame_dir.mkdir(parents=True, exist_ok=True)
            frame_prefix = frame_dir / 'frame'
        else:
            frame_prefix = None

        super().setup(fig, outfile, dpi, frame_prefix)
        self._clear_temp = False

    def grab_frame(self, **savefig_kwargs):
        if self.embed_frames:
            # Just stop processing if we hit the limit
            if self._hit_limit:
                return
            f = BytesIO()
            self.fig.savefig(f, format=self.frame_format,
                             dpi=self.dpi, **savefig_kwargs)
            imgdata64 = base64.encodebytes(f.getvalue()).decode('ascii')
            self._total_bytes += len(imgdata64)
            if self._total_bytes >= self._bytes_limit:
                _log.warning(
                    "Animation size has reached %s bytes, exceeding the limit "
                    "of %s. If you're sure you want a larger animation "
                    "embedded, set the animation.embed_limit rc parameter to "
                    "a larger value (in MB). This and further frames will be "
                    "dropped.", self._total_bytes, self._bytes_limit)
                self._hit_limit = True
            else:
                self._saved_frames.append(imgdata64)
        else:
            return super().grab_frame(**savefig_kwargs)

    def finish(self):
        # save the frames to an html file
        if self.embed_frames:
            fill_frames = _embedded_frames(self._saved_frames,
                                           self.frame_format)
            Nframes = len(self._saved_frames)
        else:
            # temp names is filled by FileMovieWriter
            fill_frames = _included_frames(self._temp_paths, self.frame_format)
            Nframes = len(self._temp_paths)
        mode_dict = dict(once_checked='',
                         loop_checked='',
                         reflect_checked='')
        mode_dict[self.default_mode + '_checked'] = 'checked'

        interval = 1000 // self.fps

        with open(self.outfile, 'w') as of:
            of.write(JS_INCLUDE + STYLE_INCLUDE)
            of.write(DISPLAY_TEMPLATE.format(id=uuid.uuid4().hex,
                                             Nframes=Nframes,
                                             fill_frames=fill_frames,
                                             interval=interval,
                                             **mode_dict))

        # duplicate the temporary file clean up logic from
        # FileMovieWriter.cleanup.  We can not call the inherited
        # versions of finished or cleanup because both assume that
        # there is a subprocess that we either need to call to merge
        # many frames together or that there is a subprocess call that
        # we need to clean up.
        if self._tmpdir:
            _log.debug('MovieWriter: clearing temporary path=%s', self._tmpdir)
            self._tmpdir.cleanup()
        else:
            if self._clear_temp:
                _log.debug('MovieWriter: clearing temporary paths=%s',
                           self._temp_paths)
                for path in self._temp_paths:
                    path.unlink()
