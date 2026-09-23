def test_subplot_factory_reapplication():
    assert maxes.subplot_class_factory(maxes.Axes) is maxes.Subplot
    assert maxes.subplot_class_factory(maxes.Subplot) is maxes.Subplot
