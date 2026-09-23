def test_single_minus_sign():
    plt.figure(figsize=(0.3, 0.3))
    plt.text(0.5, 0.5, '$-$')
    plt.gca().spines[:].set_visible(False)
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])

    buff = io.BytesIO()
    plt.savefig(buff, format="rgba", dpi=1000)
    array = np.frombuffer(buff.getvalue(), dtype=np.uint8)

    # If this fails, it would be all white
    assert not np.all(array == 0xff)
