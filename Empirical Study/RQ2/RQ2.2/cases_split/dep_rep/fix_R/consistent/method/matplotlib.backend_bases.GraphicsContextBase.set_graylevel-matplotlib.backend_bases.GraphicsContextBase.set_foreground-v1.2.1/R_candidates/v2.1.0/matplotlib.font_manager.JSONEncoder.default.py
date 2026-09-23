    def default(self, o):
        if isinstance(o, FontManager):
            return dict(o.__dict__, _class='FontManager')
        elif isinstance(o, FontEntry):
            return dict(o.__dict__, _class='FontEntry')
        else:
            return super(JSONEncoder, self).default(o)
