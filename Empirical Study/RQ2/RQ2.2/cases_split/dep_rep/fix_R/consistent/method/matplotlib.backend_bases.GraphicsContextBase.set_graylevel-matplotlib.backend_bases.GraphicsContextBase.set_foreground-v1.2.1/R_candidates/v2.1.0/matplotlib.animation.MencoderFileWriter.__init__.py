    @deprecated('2.0', message=mencoder_dep)
    def __init__(self, *args, **kwargs):
        with rc_context(rc={'animation.codec': 'mpeg4'}):
            super(MencoderFileWriter, self).__init__(*args, **kwargs)
