def get_examples_from_docstring(docstr):
    """
    Extracts all runnable python code from the examples
    in docstrings; returns a list of lines.
    """
    examples = doctest.DocTestParser().get_examples(docstr)
    return [f'    {l}' for e in examples for l in e.source.splitlines()]
