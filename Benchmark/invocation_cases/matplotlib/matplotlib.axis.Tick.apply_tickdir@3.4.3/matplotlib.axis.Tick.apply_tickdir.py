from matplotlib.axis import Tick
from matplotlib.lines import Line2D
import inspect

class DummyTick(Tick):
    def __init__(self):
        self._tickdir = None
        self._size = 3
        self._base_pad = 0
        self._pad = 0

        self._animated = False
        self._stale = False
        self.stale_callback = None

    def get_tick_padding(self):
        if self._tickdir == 'in':
            return 0
        return self._size

def main():
    tick = DummyTick()
    tick.apply_tickdir('in')
    print("apply_tickdir successfully called on DummyTick")
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tick.apply_tickdir))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()