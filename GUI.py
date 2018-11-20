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
        self.frontCanvas.grid(row=0, column=0, rowspan=8, sticky='w')
        self.sideCanvas.grid(row=8, column=0, sticky='w')

        #OpenPose Paramas
        self.params = self.set_params()
        self.openpose = OpenPose(self.params)

        #Label
        self.lb_color = {0:'red', 1:'#ffcc00', 2:'gray'}
        self.lb_downtxt = tkinter.Label(self.window, text='下', font=('Arial', 15), width=15)
        self.lb_prepare = tkinter.Label(self.window, text='請至定位準備', font=('Arial', 15), bg=self.lb_color[2], width=15)
        self.lb_catch = tkinter.Label(self.window, text='請彎腰握槓', font=('Arial', 15), bg=self.lb_color[2], width=15)
        self.lb_ready = tkinter.Label(self.window, text='預備', font=('Arial', 15), bg=self.lb_color[2], width=15)
        self.lb_start = tkinter.Label(self.window, text='啟動', font=('Arial', 15), bg=self.lb_color[2], width=15)
        self.lb_end = tkinter.Label(self.window, text='回復', font=('Arial', 15), bg=self.lb_color[2], width=15)
        self.lb = [self.lb_prepare, self.lb_catch, self.lb_ready, self.lb_start, self.lb_end]

        self.lb_downtxt.grid(row=1, column=2, padx=3, pady=3, sticky='nes')
        self.lb_prepare.grid(row=2, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        self.lb_catch.grid(row=3, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        self.lb_ready.grid(row=4, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        self.lb_start.grid(row=5, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        self.lb_end.grid(row=6, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')

        # Button
        self.btn_start = tkinter.Button(self.window, text="開始偵測", font=('Arial', 15), width=15, command=self.start)
        self.btn_start.grid(row=0, column=1, padx=3, pady=3, sticky='nesw')
        self.btn_end = tkinter.Button(self.window, text="結束偵測", font=('Arial', 15), width=15, command=self.end)
        self.btn_end.grid(row=0, column=2, padx=3, pady=3, sticky='nesw')

        #Points
        self.frontPoints=np.zeros((3, 25))
        self.sidePoints=np.zeros((3, 25))

        #Human Status
        self.status = 0
        self.started = False
        self.worker = None

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.window.mainloop()

    def start(self):
        if self.started:
            print("exist")
        self.started = True
        self.worker = Thread(target=self.flow, args=())
        self.worker.start()
        # if self.worker is None or not self.worker.is_alive():
        #     self.worker = Thread(target=self.flow, args=())
        #     self.worker.start()
        # else:
        #     print("exist")

    def end(self):
        if self.started:
            for i in self.lb:
                i.config(bg=self.lb_color[2])
            self.started = False
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
        params["default_model_folder"] = dir_path + "/../../../models/"
        return params

    def flow(self):
        var_err = tkinter.StringVar()
        var_down = tkinter.IntVar()
        self.lb_down = tkinter.Label(self.window, textvariable=var_down, font=('Arial', 15), width=15)
        self.lb_down.grid(row=1, column=1, padx=3, pady=3, sticky='new')
        self.lb_error = tkinter.Label(self.window, textvariable=var_err, font=('Arial', 15), fg=self.lb_color[0], width=15)
        self.lb_error.grid(row=7, column=1, columnspan=2, padx=3, pady=3, sticky='nesw')
        i = 0
        j = 0

        while self.started:
            frontView = human.Human(self.frontPoints)
            sideView = human.Human(self.sidePoints)
            var_down.set(i)
            if self.status>0:
                self.lb[self.status-1].config(bg=self.lb_color[2])
            if self.status>4:
                i += 1
                self.status = 2
            self.lb[self.status].config(bg=self.lb_color[1])

            time.sleep(1.5)
            var_err.set('')
            print("status:", self.status)

            if self.status == 0:
                if j<3:
                    try:
                        if(frontView.measureShouldersAndAnleesParallel() == 0):
                            var_err.set('肩膀和雙腳請保持平行')
                            j = 0
                            continue
                    except ZeroDivisionError as e:
                        continue
                    if(frontView.measureShouldersAndAnkles() == 0):
                        var_err.set('雙腳需超出肩膀寬度，請在打開一點')
                        j = 0
                        continue
                    j += 1
                    time.sleep(0.3)
                    continue
                tarch_s = frontView.getTArch()
                barch_s = sideView.getBArch()
                self.status += 1
                continue

            if self.status == 1:
                if(sideView.measureHandAndKnee() == 0):
                    var_err.set('膝蓋沒有超出手臂')
                    continue
                if(sideView.measureHipAndKnee() == 0):
                    var_err.set('臀位過高')
                    continue
                if(frontView.measureWristsAndAnkles() == 0):
                    var_err.set('手請再握寬一點')
                    continue
                self.status += 1
                continue

            if self.status == 2:
                if(sideView.measureHandAndKnee() == 0):
                    var_err.set('膝蓋沒有超出手臂')
                    continue
                if(sideView.measureHipAndKnee() == 0):
                    var_err.set('臀位過高')
                    continue
                if(frontView.measureWristsAndAnkles() == 0):
                    var_err.set('手請再握寬一點')
                    continue
                if(sideView.measureArmAndBent() == 0):
                    var_err.set('手臂請打直')
                    continue
                if(sideView.measureRoundedShoulders() == 0):
                    var_err.set('圓背')
                    continue
                tarch_e = frontView.getTArch()
                self.status += 1
                continue

            if self.status == 3:
                if(frontView.measureWristsAndAnkles() == 0):
                    var_err.set('手請再握寬一點')
                    continue
                if(sideView.measureArmAndBent() == 0):
                    var_err.set('手臂請打直')
                    continue
                if(frontView.measureTArch(tarch_s)):
                    tarch_e = frontView.getTArch()
                    if(frontView.measureShouldersAndAnleesParallel() == 0):
                        var_err.set('肩膀和雙腳請保持平行')
                    if(sideView.measureBack(barch_s[0][0]) == 0):
                        var_err.set('圓背')
                    if(sideView.measureNeckAndBottom(tarch_s, tarch_e) == 0):
                        var_err.set('脖子與臀位缺乏連動性')
                    self.status += 1
                    continue
                continue

            if self.status == 4:
                self.status += 1
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

