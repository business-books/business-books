def mark_hand_center(frame_in,cont):    
    max_d=0
    pt=(0,0)
    x,y,w,h = cv2.boundingRect(cont)
    for ind_y in xrange(int(y+0.3*h),int(y+0.8*h)): #around 0.25 to 0.6 region of height (Faster calculation with ok results)
        for ind_x in xrange(int(x+0.3*w),int(x+0.6*w)): #around 0.3 to 0.6 region of width (Faster calculation with ok results)
            dist= cv2.pointPolygonTest(cont,(ind_x,ind_y),True)
            if(dist>max_d):
                max_d=dist
                pt=(ind_x,ind_y)
    if(max_d>radius_thresh*frame_in.shape[1]):
        thresh_score=True
        cv2.circle(frame_in,pt,int(max_d),(255,0,0),2)
    else:
        thresh_score=False
    return frame_in,pt,max_d,thresh_score

# 6. Find and display gesture 

def draw_humans(npimg, humans, imgcopy=False):
        if imgcopy:
            npimg = np.copy(npimg)
        image_h, image_w = npimg.shape[:2]
        centers = {}
        for human in humans:
            # draw point
            for i in range(common.CocoPart.Background.value):
                if i not in human.body_parts.keys():
                    continue

                body_part = human.body_parts[i]
                center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
                centers[i] = center
                cv2.circle(npimg, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)

            # draw line
            for pair_order, pair in enumerate(common.CocoPairsRender):
                if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
                    continue

                npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)

        return npimg 
      
      def draw_limbs(image, pose_2d, visible):
    """Draw the 2D pose without the occluded/not visible joints."""

    _COLORS = [
        [0, 0, 255], [0, 170, 255], [0, 255, 170], [0, 255, 0],
        [170, 255, 0], [255, 170, 0], [255, 0, 0], [255, 0, 170],
        [170, 0, 255]
    ]
    _LIMBS = np.array([0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9,
                       9, 10, 11, 12, 12, 13]).reshape((-1, 2))

    _NORMALISATION_FACTOR = int(math.floor(math.sqrt(image.shape[0] * image.shape[1] / NORMALISATION_COEFFICIENT)))

    for oid in range(pose_2d.shape[0]):
        for lid, (p0, p1) in enumerate(_LIMBS):
            if not (visible[oid][p0] and visible[oid][p1]):
                continue
            y0, x0 = pose_2d[oid][p0]
            y1, x1 = pose_2d[oid][p1]
            cv2.circle(image, (x0, y0), JOINT_DRAW_SIZE *_NORMALISATION_FACTOR , _COLORS[lid], -1)
            cv2.circle(image, (x1, y1), JOINT_DRAW_SIZE*_NORMALISATION_FACTOR , _COLORS[lid], -1)
            cv2.line(image, (x0, y0), (x1, y1),
                     _COLORS[lid], LIMB_DRAW_SIZE*_NORMALISATION_FACTOR , 16) 
