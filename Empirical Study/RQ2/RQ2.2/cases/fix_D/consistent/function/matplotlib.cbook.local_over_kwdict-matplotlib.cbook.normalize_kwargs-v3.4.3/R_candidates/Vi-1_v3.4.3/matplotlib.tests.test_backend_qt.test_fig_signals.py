@pytest.mark.backend('Qt5Agg', skip_on_importerror=True)
def test_fig_signals(qt_core):
    # Create a figure
    plt.figure()

    # Access signals
    event_loop_signal = None

    # Callback to fire during event loop: save SIGINT handler, then exit
    def fire_signal_and_quit():
        # Save event loop signal
        nonlocal event_loop_signal
        event_loop_signal = signal.getsignal(signal.SIGINT)

        # Request event loop exit
        qt_core.QCoreApplication.exit()

    # Timer to exit event loop
    qt_core.QTimer.singleShot(0, fire_signal_and_quit)

    # Save original SIGINT handler
    original_signal = signal.getsignal(signal.SIGINT)

    # Use our own SIGINT handler to be 100% sure this is working
    def CustomHandler(signum, frame):
        pass

    signal.signal(signal.SIGINT, CustomHandler)

    # mainloop() sets SIGINT, starts Qt event loop (which triggers timer and
    # exits) and then mainloop() resets SIGINT
    matplotlib.backends.backend_qt5._BackendQT5.mainloop()

    # Assert: signal handler during loop execution is signal.SIG_DFL
    assert event_loop_signal == signal.SIG_DFL

    # Assert: current signal handler is the same as the one we set before
    assert CustomHandler == signal.getsignal(signal.SIGINT)

    # Reset SIGINT handler to what it was before the test
    signal.signal(signal.SIGINT, original_signal)
