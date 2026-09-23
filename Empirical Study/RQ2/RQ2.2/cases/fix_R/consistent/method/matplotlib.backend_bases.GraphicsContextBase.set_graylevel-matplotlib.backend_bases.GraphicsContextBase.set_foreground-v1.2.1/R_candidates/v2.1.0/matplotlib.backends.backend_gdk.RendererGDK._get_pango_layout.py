    def _get_pango_layout(self, s, prop):
        """
        Create a pango layout instance for Text 's' with properties 'prop'.
        Return - pango layout (from cache if already exists)

        Note that pango assumes a logical DPI of 96
        Ref: pango/fonts.c/pango_font_description_set_size() manual page
        """
        # problem? - cache gets bigger and bigger, is never cleared out
        # two (not one) layouts are created for every text item s (then they
        # are cached) - why?

        key = self.dpi, s, hash(prop)
        value = self.layoutd.get(key)
        if value != None:
            return value

        size = prop.get_size_in_points() * self.dpi / 96.0
        size = np.round(size)

        font_str = '%s, %s %i' % (prop.get_name(), prop.get_style(), size,)
        font = pango.FontDescription(font_str)

        # later - add fontweight to font_str
        font.set_weight(self.fontweights[prop.get_weight()])

        layout = self.gtkDA.create_pango_layout(s)
        layout.set_font_description(font)
        inkRect, logicalRect = layout.get_pixel_extents()

        self.layoutd[key] = layout, inkRect, logicalRect
        return layout, inkRect, logicalRect
