@pytest.fixture
def chunk_limit_setup():
    N = 100_000
    dpi = 500
    w = 5*dpi
    h = 6*dpi

    # just fit in the width
    x = np.linspace(0, w, N)
    # and go top-to-bottom
    y = np.ones(N) * h
    y[::2] = 0

    idt = IdentityTransform()
    # make a renderer
    ra = RendererAgg(w, h, dpi)
    # setup the minimal gc to draw a line
    gc = ra.new_gc()
    gc.set_linewidth(1)
    gc.set_foreground('r')
    # make a Path
    p = Path(np.vstack((x, y)).T)
    # effectively disable path simplification (but leaving it "on")
    p.simplify_threshold = 0

    return ra, gc, p, idt
