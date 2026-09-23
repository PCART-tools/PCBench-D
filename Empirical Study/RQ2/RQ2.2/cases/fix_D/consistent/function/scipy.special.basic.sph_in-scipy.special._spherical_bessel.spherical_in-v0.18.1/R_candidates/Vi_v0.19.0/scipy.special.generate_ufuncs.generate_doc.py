def generate_doc(name, specs):
    tab = " "*4
    doc = ["- :py:func:`~scipy.special.{}`::\n".format(name)]
    for spec in specs:
        incodes, outcodes = spec.split("->")
        incodes = incodes.split("*")
        intypes = list(map(lambda x: CY_TYPES[x], incodes[0]))
        if len(incodes) > 1:
            types = map(lambda x: "{} *".format(CY_TYPES[x]), incodes[1])
            intypes.extend(types)
        outtype = CY_TYPES[outcodes]
        line = "{} {}({})".format(outtype, name, ", ".join(intypes))
        doc.append(2*tab + line)
    doc[-1] = "{}\n".format(doc[-1])
    doc = "\n".join(doc)
    return doc
