    def _get_xobject_symbol_name(self, filename, symbol_name):
        Fx = self.fontName(filename)
        return "-".join([
            Fx.name.decode(),
            os.path.splitext(os.path.basename(filename))[0],
            symbol_name])
