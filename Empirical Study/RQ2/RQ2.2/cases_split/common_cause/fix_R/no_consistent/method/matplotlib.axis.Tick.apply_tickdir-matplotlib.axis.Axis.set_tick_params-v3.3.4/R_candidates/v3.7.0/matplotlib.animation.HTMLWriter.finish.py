    def finish(self):
        # save the frames to an html file
        if self.embed_frames:
            fill_frames = _embedded_frames(self._saved_frames,
                                           self.frame_format)
            frame_count = len(self._saved_frames)
        else:
            # temp names is filled by FileMovieWriter
            frame_count = len(self._temp_paths)
            fill_frames = _included_frames(
                frame_count, self.frame_format,
                self._temp_paths[0].parent.relative_to(self.outfile.parent))
        mode_dict = dict(once_checked='',
                         loop_checked='',
                         reflect_checked='')
        mode_dict[self.default_mode + '_checked'] = 'checked'

        interval = 1000 // self.fps

        with open(self.outfile, 'w') as of:
            of.write(JS_INCLUDE + STYLE_INCLUDE)
            of.write(DISPLAY_TEMPLATE.format(id=uuid.uuid4().hex,
                                             Nframes=frame_count,
                                             fill_frames=fill_frames,
                                             interval=interval,
                                             **mode_dict))

        # Duplicate the temporary file clean up logic from
        # FileMovieWriter.finish.  We can not call the inherited version of
        # finish because it assumes that there is a subprocess that we either
        # need to call to merge many frames together or that there is a
        # subprocess call that we need to clean up.
        if self._tmpdir:
            _log.debug('MovieWriter: clearing temporary path=%s', self._tmpdir)
            self._tmpdir.cleanup()
