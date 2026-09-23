def test_docstring_addition():
    @_preprocess_data()
    def funcy(ax, *args, **kwargs):
        """Funcy does nothing"""

    assert re.search(r"every other argument", funcy.__doc__)
    assert not re.search(r"the following arguments", funcy.__doc__)

    @_preprocess_data(replace_names=[])
    def funcy(ax, x, y, z, bar=None):
        """Funcy does nothing"""

    assert not re.search(r"every other argument", funcy.__doc__)
    assert not re.search(r"the following arguments", funcy.__doc__)

    @_preprocess_data(replace_names=["bar"])
    def funcy(ax, x, y, z, bar=None):
        """Funcy does nothing"""

    assert not re.search(r"every other argument", funcy.__doc__)
    assert not re.search(r"the following arguments .*: \*bar\*\.",
                         funcy.__doc__)

    @_preprocess_data(replace_names=["x", "t"])
    def funcy(ax, x, y, z, t=None):
        """Funcy does nothing"""

    assert not re.search(r"every other argument", funcy.__doc__)
    assert not re.search(r"the following arguments .*: \*x\*, \*t\*\.",
                         funcy.__doc__)
