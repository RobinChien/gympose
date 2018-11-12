import os
import sys
import cv2
import math
import time
import human
import camera
from sys import platform
from imutils.video import FPS
from imutils.video import VideoStream

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append('/home/supergan/Codelab/openpose/python')

try:
    from openpose import *
except:
    raise Exception('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')

def set_params():
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
    print(params["default_model_folder"])
    return params

def main():
    params = set_params()
    openpose = OpenPose(params)
    
    #Chose Camera, 0=front, 1=side camera
    frontCam = camera.WebcamVideoStream(0).start()
    sideCam = camera.WebcamVideoStream(1).start()
    
    # OpenCV object tracker objects
    tracker = cv2.TrackerCSRT_create()
    # initialize the bounding box coordinates of the object we are going
    # to track
    initBB = None
    # initialize the FPS throughput estimator
    fps = None
    ib = 0
    while 1:
        
        #Press q key, then Break Loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        #Image Shot from Camera, ret=True or False(Success or Fail), img=sigle frame
        img_0 = frontCam.read()
        img_1 = sideCam.read()
        
        #Input Image into OpenPose, Output Keypoints and Keypoint Image
        frontPoints, frontImage = openpose.forward(img_0, True)
        sidePoints, sideImage = openpose.forward(img_1, True)
        
        if initBB is None: 
            initBB = (127,0,10,10)
            tracker.init(sideImage, initBB)
            fps = FPS().start() 
        
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(sideImage)

        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(sideImage, (x, y), (x + w, y + h),(0, 255, 0), 2)

        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on
        # the frame
        info = [
                    ("FPS", "{:.2f}".format(fps.fps())),
                ]

                # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(sideImage, text, (10, 480 - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        #Show Image
        cv2.imshow('Cam0 Human Pose Estimation', frontImage)
        cv2.imshow('Cam1 Human Pose Estimation', sideImage)
        
        if len(frontPoints)<=0 or len(sidePoints)<=0:
            print('No Human Detect!')
            continue
        
        frontView = human.Human(frontPoints)
        sideView = human.Human(sidePoints)

        
        try:
            #print("1 m_WristsAndAnkles:", frontView.measureWristsAndAnkles())
            #print("2 m_Shoulders And Anless Parallel:", frontView.measureShouldersAndAnleesParallel())
            #print("3 m_Shoulder And Ankles:", frontView.measureShouldersAndAnkles())
            #if(ib == 0):
                #ib = frontView.getInitBack()
            
            #print(frontView.measureBack(ib['IB']))
            #print(frontView.getInitialBack())
            print(frontView.measureArmBent())
            print('\n')
        except ZeroDivisionError as e:
            print("ZeroDivisionError:", e)
            continue

    #Release Camera
    frontCam.stop()
    sideCam.stop()
    
    #Close All OpenCV Windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
