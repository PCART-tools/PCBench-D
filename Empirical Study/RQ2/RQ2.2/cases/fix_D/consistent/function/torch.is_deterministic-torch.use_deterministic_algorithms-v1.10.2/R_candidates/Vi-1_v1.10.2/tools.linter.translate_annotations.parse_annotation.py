def parse_annotation(regex: Pattern[str], line: str) -> Optional[Annotation]:
    m = re.match(regex, line)
    if m:
        try:
            line_number = int(m.group('lineNumber'))
            column_number = int(m.group('columnNumber'))
        except ValueError:
            return None
        return {
            'filename': m.group('filename'),
            'lineNumber': line_number,
            'columnNumber': column_number,
            'errorCode': m.group('errorCode'),
            'errorDesc': m.group('errorDesc'),
        }
    else:
        return None
