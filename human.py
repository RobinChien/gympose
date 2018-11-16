import math
import numpy as np

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
        return np.array([[self.Neck], [self.RS], [self.LS], [self.MH]])
    
    def measureTArch(self, tarch):
        t = np.absolute(self.getTArch()-tarch)
        print("measureTArch:", t)
        if t.any()>5:
            return 0
        return 1

    #手腕有無超出腳踝
    def measureWristsAndAnkles(self):
        hwidth = abs(self.RW[0]-self.LW[0])
        fwidth = abs(self.RA[0]-self.LA[0])
        print("mWAA_hwidth", hwidth)
        print("mWAA_fwidth", fwidth)
        if hwidth > fwidth:
            return 1
        else:
            return 0
    
    #肩膀有無和雙腳平行
    def measureShouldersAndAnleesParallel(self):
        ans = self.LS-self.RS
        results= float(ans[1])/float(ans[0])
        ans2 = self.LA-self.RA
        results2= float(ans2[1])/float(ans2[0])
        if abs(results-results2)<0.15:
            return 1
        else:
            return 0		

    #雙腳間距有無超出肩膀寬度
    def measureShouldersAndAnkles(self):
        sxx=math.pow((self.RS[0]-self.LS[0]), 2)
        syy=math.pow((self.RS[1]-self.LS[1]), 2)
        s_dis=math.sqrt(sxx+syy)
        print("mSAA_sxx", sxx)
        print("mSAA_syy", syy)
        axx=math.pow((self.RA[0]-self.LA[0]), 2)
        ayy=math.pow((self.RA[1]-self.LA[1]), 2)
        print("mSAA_axx", axx)
        print("mSAA_ayy", ayy)
        a_dis=math.sqrt(axx+ayy)
        print("mSAA_sdis", s_dis)
        print("mSAA_adis", a_dis)
        if a_dis>=s_dis:
            return 1
        else:
            return 0

    #膝蓋有沒有超出手
    def measureHandAndKnee(self):
        a=self.LW[1]-self.LS[1]
        print("mHAK_a", a)
        b=self.LS[0]-self.LW[0]
        print("mHAK_b", b)
        c=(self.LW[0]*self.LS[1])-(self.LS[0]*self.LW[1])
        print("mHAK_c", c)
        e=math.sqrt((a*a)+(b*b))
        print("mHAK_e", e)
        d=abs((a*self.LK[0])+(b*self.LK[1])+c)/e
        print("mHAK_d", d)
        if self.LS[0] <= self.LK[0]:
            print("1")
            if self.LW[0] <= self.LK[0]:
                print("2")
                if d>0:
                    print(3)
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0
				
    def measureArmAndBent(self):		
        
        ans3 = np.absolute(np.around(self.LS)-np.around(self.LE))
        print("mAAB_LS", self.LS)
        print("mAAB_LE", self.LE)
        results2= float(ans3[0])/float(ans3[1])		
        
        ans4 = np.absolute(np.around(self.LE)-np.around(self.LW))
        print("mAAB_LE", self.LE)
        print("mAAB_LW", self.LW)
        results3= float(ans4[0])/float(ans4[1])		
        
        print("results2", results2)
        print("results3", results3)

        if abs(results2-results3)<0.2:
            print("mAAB_LS", self.LS)
            return 1
        else:
            return 0

    def measureHipAndKnee(self):
        mh = self.MH[1]
        lk = self.LK[1]

        if (mh-lk<0.2):
            return 1
        return 0
                
    #get initial back
    def getInitBack(self):
        print('gIB_Neck', self.Neck)
        print('gIB_MH', self.MH)
        bh=math.pow((self.Neck[0]-self.MH[0]), 2)
        bw=math.pow((self.Neck[1]-self.MH[1]), 2)
        print("gIB_bh", bh)
        print("gIB_bw", bw)
        ib=math.sqrt(bh+bw)
        print("gIB_ib", ib)

        return np.array([[ib], self.Neck, self.MH, self.LK])


    #measure Back
    def measureBack(self, ib):
        
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

    #measure if neck and bottom back at the same time
    def measureNeckAndBottom(self, ineck, ibottom, iknee):
        difNeck = abs(self.Neck[0]-ineck[0])
        difBottom = abs(self.MH[0]-ibottom[0])
        difKnee = abs(self.LK[0]-iknee[0])

        if difNeck<0.15 and difBottom<0.15 and difKnee<0.15: #both back
           return 1
        else: 
            return 0
