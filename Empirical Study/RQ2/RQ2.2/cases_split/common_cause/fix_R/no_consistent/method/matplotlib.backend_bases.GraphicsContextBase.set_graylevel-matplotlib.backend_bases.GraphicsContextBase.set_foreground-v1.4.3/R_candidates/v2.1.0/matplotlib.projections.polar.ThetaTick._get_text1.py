    def _get_text1(self):
        t = super(ThetaTick, self)._get_text1()
        t.set_rotation_mode('anchor')
        t.set_transform(t.get_transform() + self._text1_translate)
        return t
