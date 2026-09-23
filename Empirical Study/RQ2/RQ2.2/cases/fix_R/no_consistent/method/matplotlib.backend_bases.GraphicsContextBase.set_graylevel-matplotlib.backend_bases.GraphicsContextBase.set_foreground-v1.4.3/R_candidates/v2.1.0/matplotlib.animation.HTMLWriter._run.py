    def _run(self):
        # make a duck-typed subprocess stand in
        # this is called by the MovieWriter base class, but not used here.
        class ProcessStandin(object):
            returncode = 0

            def communicate(self):
                return '', ''

        self._proc = ProcessStandin()

        # save the frames to an html file
        if self.embed_frames:
            fill_frames = _embedded_frames(self._saved_frames,
                                           self.frame_format)
        else:
            # temp names is filled by FileMovieWriter
            fill_frames = _included_frames(self._temp_names,
                                           self.frame_format)

        mode_dict = dict(once_checked='',
                         loop_checked='',
                         reflect_checked='')
        mode_dict[self.default_mode + '_checked'] = 'checked'

        interval = 1000 // self.fps

        with open(self.outfile, 'w') as of:
            of.write(JS_INCLUDE)
            of.write(DISPLAY_TEMPLATE.format(id=uuid.uuid4().hex,
                                             Nframes=len(self._temp_names),
                                             fill_frames=fill_frames,
                                             interval=interval,
                                             **mode_dict))
