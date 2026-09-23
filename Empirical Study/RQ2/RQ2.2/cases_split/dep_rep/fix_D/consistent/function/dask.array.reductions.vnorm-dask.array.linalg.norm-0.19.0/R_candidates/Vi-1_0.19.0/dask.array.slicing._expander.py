@memoize
def _expander(where):
    if not where:
        def expand(seq, val):
            return seq
        return expand
    else:
        decl = """def expand(seq, val):
            return ({left}) + tuple({right})
        """
        left = []
        j = 0
        for i in range(max(where) + 1):
            if i in where:
                left.append("val, ")
            else:
                left.append("seq[%d], " % j)
                j += 1
        right = "seq[%d:]" % j
        left = "".join(left)
        decl = decl.format(**locals())
        ns = {}
        exec(compile(decl, "<dynamic>", "exec"), ns, ns)
        return ns['expand']
