def test_simple():
    fig = plt.figure()
    pickle.dump(fig, BytesIO(), pickle.HIGHEST_PROTOCOL)

    ax = plt.subplot(121)
    pickle.dump(ax, BytesIO(), pickle.HIGHEST_PROTOCOL)

    ax = plt.axes(projection='polar')
    plt.plot(np.arange(10), label='foobar')
    plt.legend()

    pickle.dump(ax, BytesIO(), pickle.HIGHEST_PROTOCOL)

#    ax = plt.subplot(121, projection='hammer')
#    pickle.dump(ax, BytesIO(), pickle.HIGHEST_PROTOCOL)

    plt.figure()
    plt.bar(x=np.arange(10), height=np.arange(10))
    pickle.dump(plt.gca(), BytesIO(), pickle.HIGHEST_PROTOCOL)

    fig = plt.figure()
    ax = plt.axes()
    plt.plot(np.arange(10))
    ax.set_yscale('log')
    pickle.dump(fig, BytesIO(), pickle.HIGHEST_PROTOCOL)
