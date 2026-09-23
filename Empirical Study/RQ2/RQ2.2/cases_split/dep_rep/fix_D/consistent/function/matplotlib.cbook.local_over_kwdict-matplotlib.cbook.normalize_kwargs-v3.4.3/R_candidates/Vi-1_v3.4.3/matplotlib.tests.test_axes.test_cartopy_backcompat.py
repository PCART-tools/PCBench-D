def test_cartopy_backcompat():

    class Dummy(matplotlib.axes.Axes):
        ...

    class DummySubplot(matplotlib.axes.SubplotBase, Dummy):
        _axes_class = Dummy

    matplotlib.axes._subplots._subplot_classes[Dummy] = DummySubplot

    FactoryDummySubplot = matplotlib.axes.subplot_class_factory(Dummy)

    assert DummySubplot is FactoryDummySubplot
