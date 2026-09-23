    def _get_text2(self):
        t = super(RadialTick, self)._get_text2()
        t.set_rotation_mode('anchor')
        return t
