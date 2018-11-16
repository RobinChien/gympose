import os
import sys
import time
import human
import camera
import tkinter
from sys import platform
from threading import Thread
from PIL import Image, ImageTk
from tkinter import ttk

class GUI:
    def __init__ (self, window, window_title='GymPose'):

        self.window = window
        self.window.title(window_title)
        self.window.geometry('970x970')
        self.frontCam = camera.WebcamVideoStream(1).start()
        self.sideCam = camera.WebcamVideoStream(0).start()

        # Create a canvas that can fit the above video source size
        self.frontCanvas = tkinter.Canvas(window, width = 533, height = 400)
        self.sideCanvas = tkinter.Canvas(window, width = 533, height = 400)
        self.frontCanvas.grid(row=0, column=0, rowspan=7, sticky='w')
        self.sideCanvas.grid(row=7, column=0, sticky='w')
       
        #OpenPose Paramas
        self.params = self.set_params()
        self.openpose = OpenPose(self.params)
       
        #Label
        self.lb_color = {0:'red', 1:'#ffcc00', 2:'green'}
        self.lb_downtxt = tkinter.Label(self.window, text='Down', font=('Arial', 15), width=15)
        self.lb_prepare = tkinter.Label(self.window, text='Please Prepare', font=('Arial', 15), width=15)
        self.lb_catch = tkinter.Label(self.window, text='Please Catch', font=('Arial', 15), width=15)
        self.lb_start = tkinter.Label(self.window, text='Please Ready', font=('Arial', 15), width=15)
        self.lb_end = tkinter.Label(self.window, text='Start', font=('Arial', 15), width=15)
        self.lb = [self.lb_prepare, self.lb_catch, self.lb_start, self.lb_end]
        
        self.lb_downtxt.grid(row=1, column=2, padx=3, pady=3, sticky='nes')
        self.lb_prepare.grid(row=2, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        self.lb_catch.grid(row=3, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        self.lb_start.grid(row=4, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        self.lb_end.grid(row=5, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        
        # Button
        self.btn_start = tkinter.Button(self.window, text="Start", font=('Arial', 15), width=15, command=self.start)
        self.btn_start.grid(row=0, column=1, padx=3, pady=3, sticky='nesw')    
        self.btn_end = tkinter.Button(self.window, text="End", font=('Arial', 15), width=15, command=self.end)
        self.btn_end.grid(row=0, column=2, padx=3, pady=3, sticky='nesw')    
       
        #Points
        self.frontPoints=np.zeros((3, 25))
        self.sidePoints=np.zeros((3, 25))

        #Human Status
        self.status = 0
        self.worker = None

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.update()
        
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.window.mainloop()

    def start(self):
        if self.worker is None or not self.worker.is_alive():
            self.worker = Thread(target=self.flow, args=()) 
            self.worker.start()
        else:
            print("exist")

    def end(self):
        if self.worker is not None:
            self.worker.join()
            print('end')

    def update(self):
        img_0 = self.frontCam.read()
        img_1 = self.sideCam.read()

        self.frontPoints, frontImage = self.openpose.forward(img_0, True)
        self.sidePoints, sideImage = self.openpose.forward(img_1, True)
        self.frontPhoto = ImageTk.PhotoImage(image = Image.fromarray(frontImage))
        self.frontCanvas.create_image(0, 0, image = self.frontPhoto, anchor = tkinter.NW)
        
        self.sidePhoto = ImageTk.PhotoImage(image = Image.fromarray(sideImage))
        self.sideCanvas.create_image(0, 0, image = self.sidePhoto, anchor = tkinter.NW)
        self.window.after(1, self.update)

    def set_params(self):
        params = dict()
        params["logging_level"] = 3
        params["output_resolution"] = "-1x-1"
        params["net_resolution"] = "-1x368"
        params["model_pose"] = "BODY_25"
        params["alpha_pose"] = 0.6
        params["scale_gap"] = 0.3
        params["scale_number"] = 1
        params["render_threshold"] = 0.05
        # If GPU version is built, and multiple GPUs are available, set the ID here
        params["num_gpu_start"] = 0
        params["disable_blending"] = False
        # Ensure you point to the correct path where models are located
        print(dir_path)
        params["default_model_folder"] = dir_path + "/../../../models/"
        return params
    
    def flow(self):
        var_err = tkinter.StringVar()
        var_down = tkinter.IntVar()
        self.lb_down = tkinter.Label(self.window, textvariable=var_down, font=('Arial', 15), width=15)
        self.lb_down.grid(row=1, column=1, padx=3, pady=3, sticky='new')
        self.lb_error = tkinter.Label(self.window, textvariable=var_err, font=('Arial', 15), width=15)
        self.lb_error.grid(row=6, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        i = 0

        while 1:
            frontView = human.Human(self.frontPoints)
            sideView = human.Human(self.sidePoints)
            var_down.set(i)
            print(type(self.status)) 
            if self.status>3:
                print(i)
                i += 1
                self.status = 2
            print(self.status)
            self.lb[self.status].config(bg=self.lb_color[1])
            if self.status>0:
                self.lb[self.status-1].config(bg=self.lb_color[2])
            time.sleep(3)
            var_err.set('')
            print("status:", self.status)

            if self.status == 0:
                try:
                    if(frontView.measureShouldersAndAnleesParallel() == 0):
                        var_err.set('肩膀和雙腳未平行')
                        continue
                except ZeroDivisionError as e:
                    continue
                if(frontView.measureShouldersAndAnkles() == 0):
                    var_err.set('雙腳間距未超出肩膀寬度')
                    continue
                tarch_s = frontView.getTArch()
                barch_s = sideView.getInitBack()
                self.status += 1
                continue
            
            if self.status == 1:
                if(frontView.measureWristsAndAnkles() == 0):
                    var_err.set('手腕未超出腳踝')
                    continue
                #if(sideView.measureHandAndKnee() == 0):
                    #var_err.set('膝蓋沒有超出手臂')
                    #continue
                if(sideView.measureHipAndKnee() == 0):
                    var_err.set('臀位過高')
                    continue
                #if(sideView.measureBack(barch_s[0][0]) == 0):
                    #var_err.set('圓背')
                    #continue
                self.status += 1
                continue
            
            if self.status == 2:
                if(sideView.measureArmAndBent() == 0):
                    var_err.set('手臂彎曲')
                    continue
                #if(sideView.measureBack(barch_s[0][0]) == 0):
                    #var_err.set('圓背')
                    #continue
                tarch_e = frontView.getTArch()
                self.status += 1
                continue

            if self.status == 3:
                if(sideView.measureArmAndBent() == 0):
                    var_err.set('手臂彎曲')
                    continue
                #if(sideView.measureBack(barch_s[0][0]) == 0):
                    #var_err.set('圓背')
                    #continue
                if(frontView.measureTArch(tarch_s)):
                    if(frontView.measureShouldersAndAnleesParallel() == 0):
                        var_err.set('肩膀和雙腳未平行')
                    if(sideView.measureNeckAndBottom(barch_s[1], barch_s[2], barch_s[3]) == 0):
                        var_err.set('脖子與臀位缺乏連動性')
                    self.status += 1
                    continue
                continue
    
    def closeWindow(self):
        self.frontCam.stop()
        self.sideCam.stop()
        self.window.destroy()
        print('exit')

if __name__=='__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append('/home/supergan/Codelab/openpose/python')
    
    try:
        from openpose import *
    except:
        raise Exception('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    
    GUI(tkinter.Tk(), 'GymPose')

