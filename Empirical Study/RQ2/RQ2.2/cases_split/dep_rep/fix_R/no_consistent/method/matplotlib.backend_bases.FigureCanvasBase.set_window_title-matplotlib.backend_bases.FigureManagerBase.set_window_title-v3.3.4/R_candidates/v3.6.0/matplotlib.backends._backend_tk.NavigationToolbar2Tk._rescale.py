    def _rescale(self):
        """
        Scale all children of the toolbar to current DPI setting.

        Before this is called, the Tk scaling setting will have been updated to
        match the new DPI. Tk widgets do not update for changes to scaling, but
        all measurements made after the change will match the new scaling. Thus
        this function re-applies all the same sizes in points, which Tk will
        scale correctly to pixels.
        """
        for widget in self.winfo_children():
            if isinstance(widget, (tk.Button, tk.Checkbutton)):
                if hasattr(widget, '_image_file'):
                    # Explicit class because ToolbarTk calls _rescale.
                    NavigationToolbar2Tk._set_image_for_button(self, widget)
                else:
                    # Text-only button is handled by the font setting instead.
                    pass
            elif isinstance(widget, tk.Frame):
                widget.configure(height='22p', pady='1p')
                widget.pack_configure(padx='4p')
            elif isinstance(widget, tk.Label):
                pass  # Text is handled by the font setting instead.
            else:
                _log.warning('Unknown child class %s', widget.winfo_class)
        self._label_font.configure(size=10)
