def single_column_table(column, align=None, style=None):
    table = '<table'
    if align is not None:
        table += (' align="%s"' % align)
    if style is not None:
        table += (' style="%s"' % style)
    table += '><tbody>'
    for i in column:
        table += ('<tr><td>%s</td></tr>' % str(i))
    table += '</tbody></table>'
    return table
