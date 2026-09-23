    def _get_text2(self):
        'Get the default Text 2 instance'
        # x in data coords, y in axes coords
        trans, vert, horiz = self._get_text2_transform()
        t = mtext.Text(
            x=0, y=1,
            fontproperties=font_manager.FontProperties(size=self._labelsize),
            color=self._labelcolor,
            verticalalignment=vert,
            horizontalalignment=horiz,
            )
        t.set_transform(trans)
        self._set_artist_props(t)
        return t
