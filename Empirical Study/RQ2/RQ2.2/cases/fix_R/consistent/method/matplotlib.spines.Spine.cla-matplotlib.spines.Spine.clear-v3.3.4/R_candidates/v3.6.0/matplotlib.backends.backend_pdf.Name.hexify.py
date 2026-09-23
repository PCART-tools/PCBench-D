    @staticmethod
    @_api.deprecated("3.6")
    def hexify(match):
        return '#%02x' % ord(match.group())
