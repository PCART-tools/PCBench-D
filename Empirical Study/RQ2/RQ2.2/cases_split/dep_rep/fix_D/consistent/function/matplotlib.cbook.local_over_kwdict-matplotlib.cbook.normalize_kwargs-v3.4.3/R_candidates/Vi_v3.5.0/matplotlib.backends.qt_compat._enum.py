@functools.lru_cache(None)
def _enum(name):
    # foo.bar.Enum.Entry (PyQt6) <=> foo.bar.Entry (non-PyQt6).
    return operator.attrgetter(
        name if QT_API == 'PyQt6' else name.rpartition(".")[0]
    )(sys.modules[QtCore.__package__])
