@pytest.mark.backend('Qt5Agg', skip_on_importerror=True)
def test_pixel_ratio_change():
    """
    Make sure that if the pixel ratio changes, the figure dpi changes but the
    widget remains the same physical size.
    """

    prop = 'matplotlib.backends.backend_qt5.FigureCanvasQT.devicePixelRatioF'
    with mock.patch(prop) as p:
        p.return_value = 3

        fig = plt.figure(figsize=(5, 2), dpi=120)
        qt_canvas = fig.canvas
        qt_canvas.show()

        def set_pixel_ratio(ratio):
            p.return_value = ratio
            # Make sure the mocking worked
            assert qt_canvas._dpi_ratio == ratio

            # The value here doesn't matter, as we can't mock the C++ QScreen
            # object, but can override the functional wrapper around it.
            # Emitting this event is simply to trigger the DPI change handler
            # in Matplotlib in the same manner that it would occur normally.
            screen.logicalDotsPerInchChanged.emit(96)

            qt_canvas.draw()
            qt_canvas.flush_events()

        qt_canvas.manager.show()
        size = qt_canvas.size()
        screen = qt_canvas.window().windowHandle().screen()
        set_pixel_ratio(3)

        # The DPI and the renderer width/height change
        assert fig.dpi == 360
        assert qt_canvas.renderer.width == 1800
        assert qt_canvas.renderer.height == 720

        # The actual widget size and figure physical size don't change
        assert size.width() == 600
        assert size.height() == 240
        assert qt_canvas.get_width_height() == (600, 240)
        assert (fig.get_size_inches() == (5, 2)).all()

        set_pixel_ratio(2)

        # The DPI and the renderer width/height change
        assert fig.dpi == 240
        assert qt_canvas.renderer.width == 1200
        assert qt_canvas.renderer.height == 480

        # The actual widget size and figure physical size don't change
        assert size.width() == 600
        assert size.height() == 240
        assert qt_canvas.get_width_height() == (600, 240)
        assert (fig.get_size_inches() == (5, 2)).all()

        set_pixel_ratio(1.5)

        # The DPI and the renderer width/height change
        assert fig.dpi == 180
        assert qt_canvas.renderer.width == 900
        assert qt_canvas.renderer.height == 360

        # The actual widget size and figure physical size don't change
        assert size.width() == 600
        assert size.height() == 240
        assert qt_canvas.get_width_height() == (600, 240)
        assert (fig.get_size_inches() == (5, 2)).all()
