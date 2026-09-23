@needs_usetex
def test_partial_usetex(caplog):
    caplog.set_level("WARNING")
    plt.figtext(.5, .5, "foo", usetex=True)
    plt.savefig(io.BytesIO(), format="ps")
    assert caplog.records and all("as if usetex=False" in record.getMessage()
                                  for record in caplog.records)
