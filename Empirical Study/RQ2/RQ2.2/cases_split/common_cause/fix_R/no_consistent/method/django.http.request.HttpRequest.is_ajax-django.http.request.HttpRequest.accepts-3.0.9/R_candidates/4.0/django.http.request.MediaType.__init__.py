    def __init__(self, media_type_raw_line):
        full_type, self.params = parse_header(
            media_type_raw_line.encode('ascii') if media_type_raw_line else b''
        )
        self.main_type, _, self.sub_type = full_type.partition('/')
