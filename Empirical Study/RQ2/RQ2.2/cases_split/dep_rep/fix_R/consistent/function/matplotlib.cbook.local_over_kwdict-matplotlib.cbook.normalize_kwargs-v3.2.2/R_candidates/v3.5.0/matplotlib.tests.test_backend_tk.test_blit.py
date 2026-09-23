@pytest.mark.backend('TkAgg', skip_on_importerror=True)
@_isolated_tk_test(success_count=6)  # len(bad_boxes)
def test_blit():  # pragma: no cover
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends import _tkagg

    fig, ax = plt.subplots()
    photoimage = fig.canvas._tkphoto
    data = np.ones((4, 4, 4))
    height, width = data.shape[:2]
    dataptr = (height, width, data.ctypes.data)
    # Test out of bounds blitting.
    bad_boxes = ((-1, 2, 0, 2),
                 (2, 0, 0, 2),
                 (1, 6, 0, 2),
                 (0, 2, -1, 2),
                 (0, 2, 2, 0),
                 (0, 2, 1, 6))
    for bad_box in bad_boxes:
        try:
            _tkagg.blit(
                photoimage.tk.interpaddr(), str(photoimage), dataptr, 0,
                (0, 1, 2, 3), bad_box)
        except ValueError:
            print("success")
