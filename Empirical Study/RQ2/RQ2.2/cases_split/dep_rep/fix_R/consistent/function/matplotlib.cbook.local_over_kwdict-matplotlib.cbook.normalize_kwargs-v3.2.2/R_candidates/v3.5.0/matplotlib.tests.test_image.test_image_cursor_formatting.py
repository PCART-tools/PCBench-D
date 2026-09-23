def test_image_cursor_formatting():
    fig, ax = plt.subplots()
    # Create a dummy image to be able to call format_cursor_data
    im = ax.imshow(np.zeros((4, 4)))

    data = np.ma.masked_array([0], mask=[True])
    assert im.format_cursor_data(data) == '[]'

    data = np.ma.masked_array([0], mask=[False])
    assert im.format_cursor_data(data) == '[0]'

    data = np.nan
    assert im.format_cursor_data(data) == '[nan]'
