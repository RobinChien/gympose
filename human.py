import math

class Human:
    def __init__(self, keypoints):
        #{0,  "Nose"},
        self.Nose = keypoints[0][0]
        #{1,  "Neck"},
        self.Neck = keypoints[0][1]
        #{2,  "RShoulder"},!!
        self.RS = keypoints[0][2]
        #{3,  "RElbow"},
        self.RE = keypoints[0][3]
        #{4,  "RWrist"},
        self.RW = keypoints[0][4]
        #{5,  "LShoulder"},!!
        self.LS = keypoints[0][5]
        #{6,  "LElbow"},
        self.LE = keypoints[0][6]
        #{7,  "LWrist"},
        self.LW = keypoints[0][7]
        #{8,  "MidHip"},
        self.MH = keypoints[0][8]
        #{9,  "RHip"},
        self.RH = keypoints[0][9]
        #{10, "RKnee"},
        self.RK = keypoints[0][10]
        #{11, "RAnkle"},!!
        self.RA = keypoints[0][11]
        #{12, "LHip"},
        self.LH = keypoints[0][12]
        #{13, "LKnee"},
        self.LK = keypoints[0][13]
        #{14, "LAnkle"},!!
        self.LA = keypoints[0][14]

        
    def getTArch(self):
        return {'RS':self.RS, 'LS':self.LS, 'Neck':self.Neck, 'MH':self.MH}
				
    def measureWristsAndAnkles(self):
        hwidth = abs(self.RW[0]-self.LW[0])
        fwidth = abs(self.RA[0]-self.LA[0])
        if hwidth > fwidth:
            return 1
        else:
            return 0
			
    def measureShouldersAndAnleesParallel(self):
		
        ans = self.LS-self.RS
        s_line = float(ans[1])/float(ans[0])

	#陣列(雙腳)
        ans2 = self.LA-self.RA
        a_line = float(ans2[1])/float(ans2[0])
        
        if abs(s_line-a_line)<0.15:
            return 1
        else:
            return 0

    def measureShouldersAndAnkles(self):
        
        sxx=math.pow((self.RS[0]-self.LS[0]), 2)
        syy=math.pow((self.RS[1]-self.LS[1]), 2)
        s_dis=math.sqrt(sxx+syy)

        axx=math.pow((self.RA[0]-self.LA[0]), 2)
        ayy=math.pow((self.RA[1]-self.LA[1]), 2)
        a_dis=math.sqrt(axx+ayy)

        if a_dis>=s_dis:
            return 1
        else:
            return 0

    def mesureHandAndKnee(self):
        a=self.RW[1]-self.RS[1]
        b=self.RS[0]-self.RW[0]
        c=(self.RW[0]*self.RS[1])-(self.RS[0]*self.RW[1])
        e=math.sqrt((a*a)+(b*b))
        d=abs((a*self.RK[0])+(b*self.RK[1])+c)/e
        if self.RS[0] <= self.RK[0]:
            if self.RW[0] <= self.RK[0]:
                if d>0:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0
				
    def measureArmBent(self):		
        
        ans3 = self.RE-self.RS
        results2= float(ans3[1])/float(ans3[0])		
        
        ans4 = self.RW-self.RE
        results3= float(ans4[1])/float(ans4[0])		
        
        if abs(results2 == results3):
            return 1
        else:
            return 0

    def measureHipAndKnee(self):
        mh = self.MH[1]
        rk = self.RK[1]

        if (mh-rk<0.2):
            return 1
        else:
            return 0

    #get initial back
    def getInitBack(self):
        bh=math.pow((self.Nose[0]-self.MH[0]), 2)
        bw=math.pow((self.Nose[1]-self.MH[1]), 2)
        ib=math.sqrt(bh+bw)

        return {'IB':ib}

    #measure Back
    def measureBack(self, ib=0):
        
        #Threshold
        th=10 

        nbh=math.pow((self.Nose[0]-self.MH[0]), 2)
        nbw=math.pow((self.Nose[1]-self.MH[1]), 2)
        nb=math.sqrt(nbh+nbw)
        
        print("ib", ib)
        diff=abs(ib-nb)
        print("diff", diff)

        if diff<th:
            return 1
        else:
            return 0
