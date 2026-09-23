    def cleanup(self):
        '''Clean-up and collect the process used to write the movie file.'''
        out, err = self._proc.communicate()
        self._frame_sink().close()
        _log.debug('MovieWriter -- Command stdout:\n%s', out)
        _log.debug('MovieWriter -- Command stderr:\n%s', err)
