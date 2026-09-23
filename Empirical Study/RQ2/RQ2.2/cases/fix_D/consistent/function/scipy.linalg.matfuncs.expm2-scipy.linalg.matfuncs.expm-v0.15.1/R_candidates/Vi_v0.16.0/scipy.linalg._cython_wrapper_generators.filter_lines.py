def filter_lines(ls):
    ls = [l.strip() for l in ls if l != '\n' and l[0] != '#']
    func_sigs = [split_signature(l) for l in ls if l.split(' ')[0] != 'void']
    sub_sigs = [split_signature(l) for l in ls if l.split(' ')[0] == 'void']
    all_sigs = list(sorted(func_sigs + sub_sigs, key=itemgetter(0)))
    return func_sigs, sub_sigs, all_sigs
