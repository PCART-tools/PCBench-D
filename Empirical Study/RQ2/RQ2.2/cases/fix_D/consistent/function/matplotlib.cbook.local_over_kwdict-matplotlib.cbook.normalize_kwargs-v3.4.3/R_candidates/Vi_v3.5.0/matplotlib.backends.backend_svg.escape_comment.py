def escape_comment(s):
    s = escape_cdata(s)
    return _escape_xml_comment.sub('- ', s)
