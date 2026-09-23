    @_api.deprecated(
        "3.3", alternative="os.path.join(mpl.get_data_path(), 'images')")
    @property
    def basedir(self):
        return str(cbook._get_data_path('images'))
