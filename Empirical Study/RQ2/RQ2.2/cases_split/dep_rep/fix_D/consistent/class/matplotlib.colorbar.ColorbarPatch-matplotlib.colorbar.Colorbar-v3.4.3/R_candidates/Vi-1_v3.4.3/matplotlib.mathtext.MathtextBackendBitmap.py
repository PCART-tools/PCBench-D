@_api.deprecated("3.4", alternative="mathtext.math_to_image")
class MathtextBackendBitmap(MathtextBackendAgg):
    def get_results(self, box, used_characters):
        ox, oy, width, height, depth, image, characters = \
            super().get_results(box, used_characters)
        return image, depth
