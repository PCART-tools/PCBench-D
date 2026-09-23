def generate_css(attrib={}):
    if attrib:
        output = StringIO()
        attrib = sorted(attrib.items())
        for k, v in attrib:
            k = escape_attrib(k)
            v = escape_attrib(v)
            output.write("%s:%s;" % (k, v))
        return output.getvalue()
    return ''
