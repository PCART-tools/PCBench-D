@keep_lazy_text
def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks. Expects that
    existing line breaks are posix newlines.

    Preserve all white space except added line breaks consume the space on
    which they break the line.

    Don't wrap long words, thus the output text may have lines longer than
    ``width``.
    """
    def _generator():
        for line in text.splitlines(True):  # True keeps trailing linebreaks
            max_width = min((line.endswith('\n') and width + 1 or width), width)
            while len(line) > max_width:
                space = line[:max_width + 1].rfind(' ') + 1
                if space == 0:
                    space = line.find(' ') + 1
                    if space == 0:
                        yield line
                        line = ''
                        break
                yield '%s\n' % line[:space - 1]
                line = line[space:]
                max_width = min((line.endswith('\n') and width + 1 or width), width)
            if line:
                yield line
    return ''.join(_generator())
