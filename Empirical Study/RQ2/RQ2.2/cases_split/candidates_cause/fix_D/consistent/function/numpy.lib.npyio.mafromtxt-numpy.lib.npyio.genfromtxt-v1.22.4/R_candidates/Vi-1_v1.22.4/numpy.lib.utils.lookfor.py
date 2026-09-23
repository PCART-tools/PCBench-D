@set_module('numpy')
def lookfor(what, module=None, import_modules=True, regenerate=False,
            output=None):
    """
    Do a keyword search on docstrings.

    A list of objects that matched the search is displayed,
    sorted by relevance. All given keywords need to be found in the
    docstring for it to be returned as a result, but the order does
    not matter.

    Parameters
    ----------
    what : str
        String containing words to look for.
    module : str or list, optional
        Name of module(s) whose docstrings to go through.
    import_modules : bool, optional
        Whether to import sub-modules in packages. Default is True.
    regenerate : bool, optional
        Whether to re-generate the docstring cache. Default is False.
    output : file-like, optional
        File-like object to write the output to. If omitted, use a pager.

    See Also
    --------
    source, info

    Notes
    -----
    Relevance is determined only roughly, by checking if the keywords occur
    in the function name, at the start of a docstring, etc.

    Examples
    --------
    >>> np.lookfor('binary representation') # doctest: +SKIP
    Search results for 'binary representation'
    ------------------------------------------
    numpy.binary_repr
        Return the binary representation of the input number as a string.
    numpy.core.setup_common.long_double_representation
        Given a binary dump as given by GNU od -b, look for long double
    numpy.base_repr
        Return a string representation of a number in the given base system.
    ...

    """
    import pydoc

    # Cache
    cache = _lookfor_generate_cache(module, import_modules, regenerate)

    # Search
    # XXX: maybe using a real stemming search engine would be better?
    found = []
    whats = str(what).lower().split()
    if not whats:
        return

    for name, (docstring, kind, index) in cache.items():
        if kind in ('module', 'object'):
            # don't show modules or objects
            continue
        doc = docstring.lower()
        if all(w in doc for w in whats):
            found.append(name)

    # Relevance sort
    # XXX: this is full Harrison-Stetson heuristics now,
    # XXX: it probably could be improved

    kind_relevance = {'func': 1000, 'class': 1000,
                      'module': -1000, 'object': -1000}

    def relevance(name, docstr, kind, index):
        r = 0
        # do the keywords occur within the start of the docstring?
        first_doc = "\n".join(docstr.lower().strip().split("\n")[:3])
        r += sum([200 for w in whats if w in first_doc])
        # do the keywords occur in the function name?
        r += sum([30 for w in whats if w in name])
        # is the full name long?
        r += -len(name) * 5
        # is the object of bad type?
        r += kind_relevance.get(kind, -1000)
        # is the object deep in namespace hierarchy?
        r += -name.count('.') * 10
        r += max(-index / 100, -100)
        return r

    def relevance_value(a):
        return relevance(a, *cache[a])
    found.sort(key=relevance_value)

    # Pretty-print
    s = "Search results for '%s'" % (' '.join(whats))
    help_text = [s, "-"*len(s)]
    for name in found[::-1]:
        doc, kind, ix = cache[name]

        doclines = [line.strip() for line in doc.strip().split("\n")
                    if line.strip()]

        # find a suitable short description
        try:
            first_doc = doclines[0].strip()
            if _function_signature_re.search(first_doc):
                first_doc = doclines[1].strip()
        except IndexError:
            first_doc = ""
        help_text.append("%s\n    %s" % (name, first_doc))

    if not found:
        help_text.append("Nothing found.")

    # Output
    if output is not None:
        output.write("\n".join(help_text))
    elif len(help_text) > 10:
        pager = pydoc.getpager()
        pager("\n".join(help_text))
    else:
        print("\n".join(help_text))
