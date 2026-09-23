    def cleanup(self):
        '''Clean-up and collect the process used to write the movie file.'''
        out, err = self._proc.communicate()
        self._frame_sink().close()
        verbose.report('MovieWriter -- '
                       'Command stdout:\n%s' % out, level='debug')
        verbose.report('MovieWriter -- '
                       'Command stderr:\n%s' % err, level='debug')
