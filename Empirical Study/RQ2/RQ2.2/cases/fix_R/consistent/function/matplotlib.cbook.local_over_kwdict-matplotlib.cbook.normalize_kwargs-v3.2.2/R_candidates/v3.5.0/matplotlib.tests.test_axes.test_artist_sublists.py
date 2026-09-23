def test_artist_sublists():
    fig, ax = plt.subplots()
    lines = [ax.plot(np.arange(i, i + 5))[0] for i in range(6)]
    col = ax.scatter(np.arange(5), np.arange(5))
    im = ax.imshow(np.zeros((5, 5)))
    patch = ax.add_patch(mpatches.Rectangle((0, 0), 5, 5))
    text = ax.text(0, 0, 'foo')

    # Get items, which should not be mixed.
    assert list(ax.collections) == [col]
    assert list(ax.images) == [im]
    assert list(ax.lines) == lines
    assert list(ax.patches) == [patch]
    assert not ax.tables
    assert list(ax.texts) == [text]

    # Get items should work like lists/tuple.
    assert ax.lines[0] is lines[0]
    assert ax.lines[-1] is lines[-1]
    with pytest.raises(IndexError, match='out of range'):
        ax.lines[len(lines) + 1]

    # Deleting items (multiple or single) should warn.
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        del ax.lines[-1]
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        del ax.lines[-1:]
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        del ax.lines[1:]
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        del ax.lines[0]

    # Lists should be empty after removing items.
    col.remove()
    assert not ax.collections
    im.remove()
    assert not ax.images
    patch.remove()
    assert not ax.patches
    text.remove()
    assert not ax.texts

    # Everything else should remain empty.
    assert not ax.lines
    assert not ax.tables

    # Adding items should warn.
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        ax.lines.append(lines[-2])
    assert list(ax.lines) == [lines[-2]]
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        ax.lines.append(lines[-1])
    assert list(ax.lines) == lines[-2:]
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        ax.lines.insert(-2, lines[0])
    assert list(ax.lines) == [lines[0], lines[-2], lines[-1]]

    # Modifying items should warn.
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        ax.lines[0] = lines[0]
    assert list(ax.lines) == [lines[0], lines[-2], lines[-1]]
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='modification of the Axes.lines property'):
        ax.lines[1:1] = lines[1:-2]
    assert list(ax.lines) == lines

    # Adding to other lists should produce a regular list.
    assert ax.lines + [1, 2, 3] == [*lines, 1, 2, 3]
    assert [1, 2, 3] + ax.lines == [1, 2, 3, *lines]
