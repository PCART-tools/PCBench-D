    def __getitem__(self, key):
        if key in ["spectral", "spectral_r"]:
            warn_deprecated(
                "2.0",
                name="spectral and spectral_r",
                alternative="nipy_spectral and nipy_spectral_r",
                obj_type="colormap"
                )
        elif key in ["Vega10", "Vega10_r", "Vega20", "Vega20_r", "Vega20b",
                     "Vega20b_r", "Vega20c", "Vega20c_r"]:
            warn_deprecated(
                "2.0",
                name=key,
                alternative="tab" + key[4:],
                obj_type="colormap"
                )

        return super(_deprecation_datad, self).__getitem__(key)
