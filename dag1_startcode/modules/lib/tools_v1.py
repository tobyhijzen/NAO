import cv
from naoqi import ALProxy
import math
import Image

class tools_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #unsubscribe from camera
    def cUnsubscribe(self):
        """ Try to unsubscribe from the camera """ 
        try:
            self.globals.vidProxy.unsubscribe("python_GVM")
        except Exception as inst:
            print "Unsubscribing impossible:", inst

    #subscribe to camera        
    def cSubscribe(self, resolution=1):
        """ Subscribe to the camera feed. """
        self.cUnsubscribe()
        self.globals.vidProxy.setParam(18,1)
        # subscribe(gvmName, resolution={0,1,2}, colorSpace={0,9,10,rgb=11,hsy=12,bgr=13}, fps={5,10,15,30}
        self.globals.vidProxy.subscribe("python_GVM", resolution, 11, 30)
       
    # get snapshot from camera
    def getSnapshot(self):
        """ snapShot() -> iplImg, (cameraPos6D, headAngles)

        Take a snapshot from the current subscribed video feed. 
        
        """
        # Get camPos
        # getPosition(name, space={0,1,2}, useSensorValues)
        camPos = self.globals.motProxy.getPosition("CameraBottom", 2, True)
        headAngles = self.globals.motProxy.getAngles(["HeadPitch", "HeadYaw"], True)   
        
        # Get image
        # shot[0]=width, shot[1]=height, shot[6]=image-data
        shot = self.globals.vidProxy.getImageRemote("python_GVM")
        size = (shot[0], shot[1])
        picture = Image.frombuffer("RGB", size, shot[6], "raw", "BGR", 0, 1)
 
        #create a open cv image of the snapshot
        image = cv.CreateImageHeader(size, cv.IPL_DEPTH_8U, 3)     
        cv.SetData(image,picture.tostring(), picture.size[0]*3)
        hsvImage = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
        cv.CvtColor(image, hsvImage, cv.CV_BGR2HSV)
        
        return (hsvImage, (camPos, headAngles))
    
    def SaveImage(self, name, img):
        cv.SaveImage(name, img)
    
    def minimizedAngle( angle ):
        """ maps an angle to the interval [pi, pi] """
        if angle > math.pi:
            angle -= 2*math.pi
        if angle <= -math.pi:
            angle += 2*math.pi
        return angle