    def _get_xobject_symbol_name(self, filename, symbol_name):
        return "%s-%s" % (
            os.path.splitext(os.path.basename(filename))[0],
            symbol_name)
