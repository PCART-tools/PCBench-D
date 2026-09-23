    def default(self, o):
        if isinstance(o, FontManager):
            return dict(o.__dict__, __class__='FontManager')
        elif isinstance(o, FontEntry):
            d = dict(o.__dict__, __class__='FontEntry')
            try:
                # Cache paths of fonts shipped with mpl relative to the mpl
                # data path, which helps in the presence of venvs.
                d["fname"] = str(
                    Path(d["fname"]).relative_to(mpl.get_data_path()))
            except ValueError:
                pass
            return d
        else:
            return super().default(o)
