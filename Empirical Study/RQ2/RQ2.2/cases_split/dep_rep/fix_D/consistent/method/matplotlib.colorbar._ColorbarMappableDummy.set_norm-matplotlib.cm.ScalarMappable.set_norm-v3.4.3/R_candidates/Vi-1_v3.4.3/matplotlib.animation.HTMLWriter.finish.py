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
