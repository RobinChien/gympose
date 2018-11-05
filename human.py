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
		
	#陣列(肩膀)
        c1=self.RS
        c2=self.LS
        #存放兩個陣列的變數
        ans = list(map(lambda x: (x[0]-x[1]), zip(c2,c1)))
        #進行陣列內第0跟1位置的計算
        results= float(ans[1])/float(ans[0])
	#得出肩膀之斜率
        #print(results)
	#印出肩膀結果

	#陣列(雙腳)
        d1=self.RA
        d2=self.LA
	#存放兩個陣列的變數
        ans2 = list(map(lambda x: (x[0]-x[1]), zip(d2,d1)))
	#進行陣列內第0跟1位置的計算
        results2= float(ans2[1])/float(ans2[0])
	#得出雙腳之斜率
        #print(results2)
	#印出雙腳結果
        if abs(results-results2)<0.15:
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
			
	def hand_knee(self):
		a=self.RW[1]-self.RS[1]
		b=self.RS[0]-self.RW[0]
		c=(self.RW[0]*self.RS[1])-(self.RS[0]*self.RW[1])
		e=math.sqrt((a*a)+(b*b))
		d=abs((a*self.RK[0])+(b*self.RK[1])+c)/e
		if self.RS[0] <= self.RK[0]:
			if self.RW[0] <= self.RK[0]:
				if d>0:
					return 1;
				else:
					return 0;
			else:
				return 0;
		else:
			return 0;
				
	def measureArmBent(self):
			
        c11=self.RS
        c22=self.RE
        c33=self.RW
        ans3 = list(map(lambda x: (x[0]-x[1]), zip(c2,c1)))        
        results2= float(ans3[1])/float(ans3[0])		
        ans4 = list(map(lambda x: (x[0]-x[1]), zip(c3,c2)))		
        results3= float(ans4[1])/float(ans4[0])		
        if abs(results2==results3):
            return 1
        else:
            return 0



    #get initial back
    def getInitialBack(self):
        bh=math.pow((self.Neck[0]-self.MH[0]), 2)
        bw=math.pow((self.Neck[1]-self.MH[1]), 2)
        ib=math.sqrt(bh+bw)

        return {'IB':ib}

    #measure Back
    def measureBack(self, ib):
        
         #Threshold
        th=0.15 

        nbh=math.pow((self.Neck[0]-self.MH[0]), 2)
        nbw=math.pow((self.Neck[1]-self.MH[1]), 2)
        nb=math.sqrt(nbh+nbw)

        diff=abs(ib-nb)

        if diff<th:
            return 1
        else:
            return 0


