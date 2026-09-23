    @staticmethod
    def _icon(name):
        """
        Construct a `wx.Bitmap` suitable for use as icon from an image file
        *name*, including the extension and relative to Matplotlib's "images"
        data directory.
        """
        image = np.array(PIL.Image.open(cbook._get_data_path("images", name)))
        try:
            dark = wx.SystemSettings.GetAppearance().IsDark()
        except AttributeError:  # wxpython < 4.1
            # copied from wx's IsUsingDarkBackground / GetLuminance.
            bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
            # See wx.Colour.GetLuminance.
            bg_lum = (.299 * bg.red + .587 * bg.green + .114 * bg.blue) / 255
            fg_lum = (.299 * fg.red + .587 * fg.green + .114 * fg.blue) / 255
            dark = fg_lum - bg_lum > .2
        if dark:
            fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
            black_mask = (image[..., :3] == 0).all(axis=-1)
            image[black_mask, :3] = (fg.Red(), fg.Green(), fg.Blue())
        return wx.Bitmap.FromBufferRGBA(
            image.shape[1], image.shape[0], image.tobytes())
