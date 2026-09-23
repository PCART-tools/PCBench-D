    def _get_text1(self):
        'Get the default Text instance'
        # x in axes coords, y in data coords
        trans, vert, horiz = self._get_text1_transform()
        t = mtext.Text(
            x=0, y=0,
            fontproperties=font_manager.FontProperties(size=self._labelsize),
            color=self._labelcolor,
            verticalalignment=vert,
            horizontalalignment=horiz,
            )
        t.set_transform(trans)
        self._set_artist_props(t)
        return t
