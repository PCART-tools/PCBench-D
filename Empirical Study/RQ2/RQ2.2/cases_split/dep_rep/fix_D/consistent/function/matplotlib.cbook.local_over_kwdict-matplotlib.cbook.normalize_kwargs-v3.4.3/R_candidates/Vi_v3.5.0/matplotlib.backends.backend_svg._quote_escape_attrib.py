def _quote_escape_attrib(s):
    return ('"' + escape_cdata(s) + '"' if '"' not in s else
            "'" + escape_cdata(s) + "'" if "'" not in s else
            '"' + escape_attrib(s) + '"')
