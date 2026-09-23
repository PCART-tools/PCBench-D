@pytest.mark.backend('TkAgg', skip_on_importerror=True)
def test_blit():
    script = """
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends import _tkagg
def evil_blit(photoimage, aggimage, offsets, bboxptr):
    data = np.asarray(aggimage)
    height, width = data.shape[:2]
    dataptr = (height, width, data.ctypes.data)
    _tkagg.blit(
        photoimage.tk.interpaddr(), str(photoimage), dataptr, offsets,
        bboxptr)

fig, ax = plt.subplots()
bad_boxes = ((-1, 2, 0, 2),
             (2, 0, 0, 2),
             (1, 6, 0, 2),
             (0, 2, -1, 2),
             (0, 2, 2, 0),
             (0, 2, 1, 6))
for bad_box in bad_boxes:
    try:
        evil_blit(fig.canvas._tkphoto,
                  np.ones((4, 4, 4)),
                  (0, 1, 2, 3),
                  bad_box)
    except ValueError:
        print("success")
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            env={**os.environ,
                 "MPLBACKEND": "TkAgg",
                 "SOURCE_DATE_EPOCH": "0"},
            timeout=_test_timeout,
            stdout=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Subprocess timed out")
    except subprocess.CalledProcessError:
        pytest.fail("Likely regression on out-of-bounds data access"
                    " in _tkagg.cpp")
    else:
        print(proc.stdout)
        assert proc.stdout.count("success") == 6  # len(bad_boxes)
