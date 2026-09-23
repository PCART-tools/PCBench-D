    @deprecated('2.0', message=mencoder_dep)
    def __init__(self, *args, **kwargs):
        with rc_context(rc={'animation.codec': 'mpeg4'}):
            super(MencoderWriter, self).__init__(*args, **kwargs)
