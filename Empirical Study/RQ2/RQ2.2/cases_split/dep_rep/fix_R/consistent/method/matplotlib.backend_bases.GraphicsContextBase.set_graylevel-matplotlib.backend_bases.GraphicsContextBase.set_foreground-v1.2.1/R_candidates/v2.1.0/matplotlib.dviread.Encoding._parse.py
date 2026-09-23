    def _parse(self, file):
        result = []

        lines = (line.split(b'%', 1)[0].strip() for line in file)
        data = b''.join(lines)
        beginning = data.find(b'[')
        if beginning < 0:
            raise ValueError("Cannot locate beginning of encoding in {}"
                             .format(file))
        data = data[beginning:]
        end = data.find(b']')
        if end < 0:
            raise ValueError("Cannot locate end of encoding in {}"
                             .format(file))
        data = data[:end]

        return re.findall(br'/([^][{}<>\s]+)', data)
