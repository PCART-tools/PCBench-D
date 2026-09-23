def _test_thread_impl():
    from concurrent.futures import ThreadPoolExecutor
    import json
    import sys

    from matplotlib import pyplot as plt, rcParams

    rcParams.update({
        "webagg.open_in_browser": False,
        "webagg.port_retries": 1,
    })
    if len(sys.argv) >= 2:  # Second argument is json-encoded rcParams.
        rcParams.update(json.loads(sys.argv[1]))

    # Test artist creation and drawing does not crash from thread
    # No other guarantees!
    fig, ax = plt.subplots()
    # plt.pause needed vs plt.show(block=False) at least on toolbar2-tkagg
    plt.pause(0.5)

    future = ThreadPoolExecutor().submit(ax.plot, [1, 3, 6])
    future.result()  # Joins the thread; rethrows any exception.

    fig.canvas.mpl_connect("close_event", print)
    future = ThreadPoolExecutor().submit(fig.canvas.draw)
    plt.pause(0.5)  # flush_events fails here on at least Tkagg (bpo-41176)
    future.result()  # Joins the thread; rethrows any exception.
    plt.close()
    fig.canvas.flush_events()  # pause doesn't process events after close
