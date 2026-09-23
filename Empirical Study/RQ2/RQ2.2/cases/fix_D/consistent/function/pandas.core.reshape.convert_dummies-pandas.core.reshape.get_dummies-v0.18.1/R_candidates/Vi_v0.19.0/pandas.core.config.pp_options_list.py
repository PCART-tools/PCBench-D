def pp_options_list(keys, width=80, _print=False):
    """ Builds a concise listing of available options, grouped by prefix """

    from textwrap import wrap
    from itertools import groupby

    def pp(name, ks):
        pfx = ('- ' + name + '.[' if name else '')
        ls = wrap(', '.join(ks), width, initial_indent=pfx,
                  subsequent_indent='  ', break_long_words=False)
        if ls and ls[-1] and name:
            ls[-1] = ls[-1] + ']'
        return ls

    ls = []
    singles = [x for x in sorted(keys) if x.find('.') < 0]
    if singles:
        ls += pp('', singles)
    keys = [x for x in keys if x.find('.') >= 0]

    for k, g in groupby(sorted(keys), lambda x: x[:x.rfind('.')]):
        ks = [x[len(k) + 1:] for x in list(g)]
        ls += pp(k, ks)
    s = '\n'.join(ls)
    if _print:
        print(s)
    else:
        return s
