    def _get_default_antialiased(self):
        # This may be overridden in a subclass.
        return mpl.rcParams['patch.antialiased']
