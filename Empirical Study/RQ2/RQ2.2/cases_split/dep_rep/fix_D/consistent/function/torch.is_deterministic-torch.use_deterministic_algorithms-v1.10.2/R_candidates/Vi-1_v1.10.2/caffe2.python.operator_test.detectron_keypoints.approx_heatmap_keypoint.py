def approx_heatmap_keypoint(heatmaps_in, bboxes_in):
    '''
Mask R-CNN uses bicubic upscaling before taking the maximum of the heat map
for keypoints. We are using bilinear upscaling, which means we can approximate
the maximum coordinate with the low dimension maximum coordinates. We would like
to avoid bicubic upscaling, because it is computationally expensive. Brown and
Lowe  (Invariant Features from Interest Point Groups, 2002) uses a method  for
fitting a 3D quadratic function to the local sample points to determine the
interpolated location of the maximum of scale space, and his experiments showed
that this provides a substantial improvement to matching and stability for
keypoint extraction. This approach uses the Taylor expansion (up to the
quadratic terms) of the scale-space function. It is equivalent with the Newton
method. This efficient method were used in many keypoint estimation algorithms
like SIFT, SURF etc...

The implementation of Newton methods with numerical analysis is straight forward
and super simple, though we need a linear solver.

    '''
    assert len(bboxes_in.shape) == 2
    N = bboxes_in.shape[0]
    assert bboxes_in.shape[1] == 4
    assert len(heatmaps_in.shape) == 4
    assert heatmaps_in.shape[0] == N
    keypoint_count = heatmaps_in.shape[1]
    heatmap_size = heatmaps_in.shape[2]
    assert heatmap_size >= 2
    assert heatmaps_in.shape[3] == heatmap_size

    keypoints_out = np.zeros((N, keypoint_count, 4))

    for k in range(N):
        x0, y0, x1, y1 = bboxes_in[k, :]
        xLen = np.maximum(x1 - x0, 1)
        yLen = np.maximum(y1 - y0, 1)
        softmax_map = scores_to_probs(heatmaps_in[k, :, :, :].copy())
        f = heatmaps_in[k]
        for j in range(keypoint_count):
            f = heatmaps_in[k][j]
            maxX = -1
            maxY = -1
            maxScore = -100.0
            maxProb = -100.0
            for y in range(heatmap_size):
                for x in range(heatmap_size):
                    score = f[y, x]
                    prob = softmax_map[j, y, x]
                    if maxX < 0 or maxScore < score:
                        maxScore = score
                        maxProb = prob
                        maxX = x
                        maxY = y

            # print(maxScore, maxX, maxY)
            # initialize fmax values of 3x3 grid
            # when 3x3 grid going out-of-bound, mirrowing around center
            fmax = [[0] * 3 for r in range(3)]
            for x in range(3):
                for y in range(3):
                    hm_x = x + maxX - 1
                    hm_y = y + maxY - 1
                    hm_x = hm_x - 2 * (hm_x >= heatmap_size) + 2 * (hm_x < 0)
                    hm_y = hm_y - 2 * (hm_y >= heatmap_size) + 2 * (hm_y < 0)
                    assert((hm_x < heatmap_size) and (hm_x >= 0))
                    assert((hm_y < heatmap_size) and (hm_y >= 0))
                    fmax[y][x] = f[hm_y][hm_x]

            # print("python fmax ", fmax)
            # b = -f'(0), A = f''(0) Hessian matrix
            b = [-(fmax[1][2] - fmax[1][0]) / 2, -
                 (fmax[2][1] - fmax[0][1]) / 2]
            A = [[fmax[1][0] - 2 * fmax[1][1] + fmax[1][2],
                  (fmax[2][2] - fmax[2][0] - fmax[0][2] + fmax[0][0]) / 4],
                 [(fmax[2][2] - fmax[2][0] - fmax[0][2] + fmax[0][0]) / 4,
                  fmax[0][1] - 2 * fmax[1][1] + fmax[2][1]]]
            # print("python A")
            # print(A)
            # solve Ax=b
            div = A[1][1] * A[0][0] - A[0][1] * A[1][0]
            if abs(div) < 0.0001:
                deltaX = 0
                deltaY = 0
                deltaScore = maxScore
            else:
                deltaY = (b[1] * A[0][0] - b[0] * A[1][0]) / div
                deltaX = (b[0] * A[1][1] - b[1] * A[0][1]) / div
                # clip delta if going out-of-range of 3x3 grid
                if abs(deltaX) > 1.5 or abs(deltaY) > 1.5:
                    scale = 1.5 / max(abs(deltaX), abs(deltaY))
                    deltaX *= scale
                    deltaY *= scale
                # score = f(0) + f'(0)*x + 1/2 * f''(0) * x^2
                #    = f(0) - b*x + 1/2*x*A*x
                deltaScore = (
                    fmax[1][1] - (b[0] * deltaX + b[1] * deltaY) +
                    0.5 * (deltaX * deltaX * A[0][0] +
                           deltaX * deltaY * A[1][0] +
                           deltaY * deltaX * A[0][1] +
                           deltaY * deltaY * A[1][1]))

            assert abs(deltaX) <= 1.5
            assert abs(deltaY) <= 1.5

            # final coordinates
            keypoints_out[k, j, :] = (
                x0 + (maxX + deltaX + .5) * xLen / heatmap_size,
                y0 + (maxY + deltaY + .5) * yLen / heatmap_size,
                deltaScore,
                maxProb,
            )

    keypoints_out = np.transpose(keypoints_out, [0, 2, 1])

    return keypoints_out
