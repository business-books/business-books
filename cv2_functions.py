def update(_=None):
    noise = cv2.getTrackbarPos('noise', 'fit line')
    n = cv2.getTrackbarPos('point n', 'fit line')
    r = cv2.getTrackbarPos('outlier %', 'fit line') / 100.0
    outn = int(n*r)

    p0, p1 = (90, 80), (w-90, h-80)
    img = np.zeros((h, w, 3), np.uint8)
    cv2.line(img, toint(p0), toint(p1), (0, 255, 0))

    if n > 0:
        line_points = sample_line(p0, p1, n-outn, noise)
        outliers = np.random.rand(outn, 2) * (w, h)
        points = np.vstack([line_points, outliers])
        for p in line_points:
            cv2.circle(img, toint(p), 2, (255, 255, 255), -1)
        for p in outliers:
            cv2.circle(img, toint(p), 2, (64, 64, 255), -1)
        func = getattr(cv2, cur_func_name)
        vx, vy, cx, cy = cv2.fitLine(np.float32(points), func, 0, 0.01, 0.01)
        cv2.line(img, (int(cx-vx*w), int(cy-vy*w)), (int(cx+vx*w), int(cy+vy*w)), (0, 0, 255))

    draw_str(img, (20, 20), cur_func_name)
    cv2.imshow('fit line', img) 
