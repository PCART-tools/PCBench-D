    def _get_text1(self):
        t = super(RadialTick, self)._get_text1()
        t.set_rotation_mode('anchor')
        return t
