    @cbook._rename_parameter("3.3", "s", "text")
    @docstring.dedent_interpd
    def annotate(self, text, xy, *args, **kwargs):
        a = mtext.Annotation(text, xy, *args, **kwargs)
        a.set_transform(mtransforms.IdentityTransform())
        if 'clip_on' in kwargs:
            a.set_clip_path(self.patch)
        self._add_text(a)
        return a
