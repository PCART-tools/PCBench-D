    def _get_text2(self):
        t = super(ThetaTick, self)._get_text2()
        t.set_rotation_mode('anchor')
        t.set_transform(t.get_transform() + self._text2_translate)
        return t
