    @cbook.deprecated("3.3")
    @property
    def params_to_disable(self):
        return [key for key in mpl.rcParams if 'keymap' in key]
