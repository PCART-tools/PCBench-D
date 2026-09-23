    def get_familyname(self):
        "Return the font family name, e.g., 'Times'"
        name = self._header.get(b'FamilyName')
        if name is not None:
            return name

        # FamilyName not specified so we'll make a guess
        name = self.get_fullname()
        extras = (br'(?i)([ -](regular|plain|italic|oblique|bold|semibold|'
                  br'light|ultralight|extra|condensed))+$')
        return re.sub(extras, '', name)
