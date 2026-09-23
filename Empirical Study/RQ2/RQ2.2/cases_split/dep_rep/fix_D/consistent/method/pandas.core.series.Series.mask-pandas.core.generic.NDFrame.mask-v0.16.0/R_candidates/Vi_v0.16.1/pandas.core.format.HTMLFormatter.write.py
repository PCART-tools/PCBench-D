    def write(self, s, indent=0):
        rs = com.pprint_thing(s)
        self.elements.append(' ' * indent + rs)
