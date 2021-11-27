def ProcessFrame(self, frame):
        # segment arm region
        segment = self.SegmentArm(frame)

        # make a copy of the segmented image to draw on
        draw = cv2.cvtColor(segment, cv2.COLOR_GRAY2RGB)

        # draw some helpers for correctly placing hand
        cv2.circle(draw,(self.imgWidth/2,self.imgHeight/2),3,[255,102,0],2)       
        cv2.rectangle(draw, (self.imgWidth/3,self.imgHeight/3), (self.imgWidth*2/3, self.imgHeight*2/3), [255,102,0],2)

        # find the hull of the segmented area, and based on that find the
        # convexity defects
        [contours,defects] = self.FindHullDefects(segment)

        # detect the number of fingers depending on the contours and convexity defects
        # draw defects that belong to fingers green, others red
        [nofingers,draw] = self.DetectNumberFingers(contours, defects, draw)

        # print number of fingers on image
        cv2.putText(draw, str(nofingers), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
        return draw 
