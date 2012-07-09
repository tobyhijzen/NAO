import time

class motion_v1():    
    globals = None
    
    # set footgaitconfig to default values
    gaitConfig        = [['MaxStepX', 0.04], \
                         ['MaxStepY', 0.14], \
                         ['MaxStepTheta', 0.35], \
                         ['MaxStepFrequency', 1.0], \
                         ['StepHeight', 0.02], \
                         ['TorsoWx', 0.0], \
                         ['TorsoWy', 0.05]]
                         
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    def init(self):
        self.setGaitConfigSimple(0.06, 0.15, 0.5, 0.02, 30, 17)
        self.setFME(False)
        
    """Set fall manager on or off"""
    def setFME(self, arg):
        try:
            self.globals.motProxy.setFallManagerEnabled(arg)
        except:
            print 'Could not switch off FallManager. '
            
    """ set parts of the footgaitconfig, order is important but it does not
    have to contain each and every option (if no value found for an option
    it will use earlier specified values) """
    def setGaitConfig( self, inputConfig ):
        i = 0
        newConfig = []

        maxConfig = self.globals.motProxy.getFootGaitConfig('Max')
        minConfig = self.globals.motProxy.getFootGaitConfig('Min')
        
        # replace all values in gaitconig by the ones given by inputconfig 
        for c in range(len( self.gaitConfig )):
            newOption = self.gaitConfig[c]

            if i < len( inputConfig ):
                if self.gaitConfig[c][0] == inputConfig[i][0]:
                
                    newOption = inputConfig[i]

                    if minConfig[c][1] > inputConfig[i][1]:
                        newOption = [inputConfig[i][0], minConfig[c][1]]
                        print 'Setting', inputConfig[i][0], 'to min boundary'
                    elif maxConfig[c][1] < inputConfig[i][1]:
                        newOption = [inputConfig[i][0], maxConfig[c][1]]
                        print 'Setting', inputConfig[i][0], 'to max boundary'
                    i += 1

            newConfig.append( newOption )
                
                       
        self.gaitConfig = newConfig

    """Set gait config coordinates"""
    def setGaitConfigSimple( self, maxStepX, maxStepY, maxStepTheta, stepHeight , step_max, step_min ):
        self.setGaitConfig( [['MaxStepX', maxStepX ],\
                             ['MaxStepY', maxStepY ],\
                             ['MaxStepTheta', maxStepTheta ],\
                             ['StepHeight', stepHeight ]]  )
        # default 30
        self.globals.motProxy.setMotionConfig([["WALK_STEP_MAX_PERIOD", step_max]]) 
         # default 21
        self.globals.motProxy.setMotionConfig([["WALK_STEP_MIN_PERIOD", step_min]])

                             
    '''
    All motions are to be specified here in alphabetical order:

    Name:                        Function:                              TODO:
    --------------------------------------------------------------------------------------------------
    backToStand()                stand up lying back down               improve speed
    bellyToStand()               stand up lying face down               improve speed

    cartesianLeft                kick that uses angle + balllocation    find thresholds or reimplement
    cartesianRight               
    changeHead(yaw, pitch)       relative headmotion                    x

    experimentalKick(angle)      heelball                               further design                

    diveLeft()                   dive towards left (keeper)             safer fall? + faster getting up?
    diveRight()                  dive towards right(keeper)             

    footLeft()                   sidestep left (keeper)                 perhaps preventing ball from
    footRight()                  sidestep right (keeper)                getting stuck between legs

    getHeadPos()                 return current [yaw,pitch]             x
    getPose()                    return current pose (belly, etc)       x 
    getRobotVelocity()           return xspeed, yspeed, rotspeed        x

    hak()                        second attempt at heelball             improvement or removal..
    hakje()                      first attempt at heelball              improvement or removal.. 
    hasFallen()                  detects the falling process            TODO: TESTING

    isWalking()                  return self.globals.motProxy.walkIsActive()    x

    keepNormalPose()             normal pose for keeper                 improve speed/lessen load on joints
    kick(angle)                  kick based on given angle              further implementation (more cases)
    kill()                       remove stiffness (body)                x
    killKnees()                  remove knee stiffness                  improve speed (safely) or use only in finished state
    killWalk()                   stops walking if active                x

    lKickAngled(angle)           kick based on given angle              improve or remove entirely (dynamic kick?)

    normalPose(force)            stand in normal pose, can be forced    improve speed (safely), arm position

    postWalkTo(x,y,angle)        nonblocking walking call               x

    rKickAngled(angle)           kick based on given angle              improve or remove entirely (dynamic kick?)

    setHead(yaw,pitch)           set head position                      improve speed? not sure if needed               
    sideLeftKick()               kick softly towards the left           is meant to be for passing, could 
    sideRightKick()                                      right          maybe be faster or speed as input?
    stance()                     keeper stance()                        reduce load on knees somehow? Not sure if possible - 
                                                                        removing knee stiffness has scary results. 
                                                                        Dont try to remove kneestiffness before consulting anyone.
    standUp()                    stand up if fallen, return fallen      x
    stiff()                      set stiffness for body                 x
    stiffKnees()                 set stiffness for knees alone          use in soul
    SWTV(x,y,t,f)                setwalktargetvelocity call             x

    walkTo(x,y,angle)            walkTo call                            x

    '''

    # Stand up from the back
    def backToStand(self):
        # lie down on back, move arms towards pushing position and legs upwards
        self.globals.motProxy.setAngles(['HeadPitch', 'HeadYaw'], [-0.4, 0.0], 0.4)
        self.globals.motProxy.post.angleInterpolation(['LShoulderPitch', 'LShoulderRoll' ,'LElbowRoll', 'LElbowYaw'],
                                  [[-0.1, 0.8],       [1, 0.5] ,      [ -1.5],        [1.9]       ],\
                                  [[0.4, 0.8],        [0.5, 0.8],     [0.5],          [0.5]],  True)                
        self.globals.motProxy.post.angleInterpolation(['RShoulderPitch', 'RShoulderRoll', 'RElbowRoll', 'RElbowYaw'],
                                  [[0, 0.8],          [-1.0, -0.5],   [1.5],          [-1.9]],
                                  [[0.5, 0.8],        [0.5, 0.8],     [0.5],          [0.5]],  True)
                                
        self.globals.motProxy.setAngles(['LHipYawPitch', 'RKneePitch', 'LKneePitch', 'RHipRoll', 'LHipRoll', 'RAnkleRoll', 'LAnkleRoll'],
                    [0             ,  0           , 0          ,  0        ,  0        ,  0          ,  0          ],  0.3)
        self.globals.motProxy.setAngles( ['LHipPitch', 'LAnklePitch', 'RHipPitch', 'RAnklePitch'],
                     [-1.5       , 0.8          , -1.5,       0.8], 0.3 )
        time.sleep(1)

        # move legs down, arms down to push
        self.globals.motProxy.setAngles(['LShoulderPitch','RShoulderPitch','RHipPitch', 'LHipPitch'],
                    [2               , 2              , -0.7        ,  -0.7        ],  0.9)
        time.sleep(0.1)
        # reset legs
        self.globals.motProxy.setAngles(['RHipPitch', 'LHipPitch'], [ -1.5, -1.5 ],  0.3 )
        time.sleep(0.2)
        # push up with arms
        self.globals.motProxy.setAngles(['RShoulderRoll', 'LShoulderRoll'], [-0.25, 0.25], 0.5 )
        self.globals.motProxy.setAngles(['LElbowRoll', 'RElbowRoll'], [0,0], 0.5)
        
        time.sleep(0.4)
        
        # twist legs around to sit with legs wide
        t = 0.4
        names = list()
        angles = list()
        times = list()
            
        names.extend(['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
        angles.extend([[2],           [-0.3],            [0.7] ,     [0.06]])
        times.extend([[t],              [t],              [t],         [t]])
        
        names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
        angles.extend([[2],           [0.3],           [-0.7] ,     [-0.05]])
        times.extend([[t],              [t],             [t],         [t]])
        
        names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[-0.7],       [-0.23],    [-1.57],      [0.8],       [0.85],        [0.06]])
        times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
        
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0.23],    [-1.57],      [0.8],       [0.85],        [-0.06]])
        times.extend([[t],        [t],         [t],          [t],           [t]])    
        self.globals.motProxy.angleInterpolation(names, angles, times, True)
        
        # move one arm backwards, one arm upwards, move legs towards body
        self.globals.motProxy.setAngles(['HeadPitch', 'HeadYaw'], [0.5, 0.0], 0.4)
        t = 0.4
        names = list()
        angles = list()
        times = list()
            
        names.extend(['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
        angles.extend([[2.085], [-0.3], [0.6764], [0.055]])
        times.extend([[t],              [t],              [t],         [t]])
        
        names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
        angles.extend([[0.56],          [0.52],          [-0.33],     [-.55]])
        times.extend([[t],              [t],             [t],         [t]])
        
        names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[-0.89],       [-0.57],   [-1.31],      [0.73],       [0.93],        [0.07]])
        times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
        
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0.54],      [-1.05],    [2.11],       [-0.13],       [-0.25]])
        times.extend([[t],        [t],         [t],          [t],           [t]])
        self.globals.motProxy.angleInterpolation(names, angles, times, True)
        
        # move legs further towards body
        t = 0.6
        names = list()
        angles = list()
        times = list()
        
        names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[-1.07],      [-0.656],   [-1.67],      [1.63 ],       [0.32],       [-0.004]])
        times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
        
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[-0.01], [-0.01],     [2.11254]    , [-1] , [0.10128598]])
        times.extend([[t],        [t],         [t],          [t],           [t]])
        self.globals.motProxy.angleInterpolation(names, angles, times, True)

        # Lift arm from ground, move right leg towards body
        t = 0.3
        names = list()
        angles = list()
        times = list()
            
        names.extend(['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
        angles.extend([[1.86205],      [-0.5913],       [0.61815],   [0.0598679]])
        times.extend([[t],              [t],              [t],         [t]])
        
        names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
        angles.extend([[0.98],          [0.531],         [-0.03],     [-0.57]])
        times.extend([[t],              [t],             [t],         [t]])
        
        names.extend(['RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[-0.73],    [-1.47],     [2],         [-0.13],      [0.15]])
        times.extend([[t],            [t],        [t],         [t],          [t]])
        
        names.extend(['LAnklePitch'])
        angles.extend([[-1.18]])
        times.extend([[t]])
        
        self.globals.motProxy.angleInterpolation(names, angles, times, True)
        
        # lift right leg further towards left
        t = 0.4
        names = list()
        angles = list()
        times = list()
        
        names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[-0.5],      [-0.2],   [-0.55],      [2.11 ],       [-1.18],       [0.07]])
        times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
        
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0.2],    [-0.55],     [2.11],       [-1.18] ,  [-0.07 ]])
        times.extend([[t],        [t],         [t],          [t],           [t]])
        self.globals.motProxy.angleInterpolation(names, angles, times, True)
        
        # move legs closer to eachother (stance)
        t = 0.2
        names = list()
        angles = list()
        times = list()
        
        names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[0],           [0],        [-0.9],      [2.11 ],       [-1.18],       [0.0]])
        times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
        
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0],        [-0.9],      [2.11 ],       [-1.18],       [0.0]])
        times.extend([[t],        [t],         [t],          [t],           [t]])
        self.globals.motProxy.angleInterpolation(names, angles, times, True)        
        
        self.normalPose(True)
        
    def bellyToStand(self):
        """Stand up from belly"""
        names = list()
        times = list()
        angles = list()
        
        names.append('HeadYaw')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.17453, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -0.22689, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ 0.28623, [ 3, -0.46667, -0.01333], [ 3, 0.36667, 0.01047]],
                        [ 0.29671, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.49567, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ -0.29671, [ 3, -0.23333, -0.07104], [ 3, 0.36667, 0.11164]],
                        [ 0.05236, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.39095, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('HeadPitch')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ -0.57683, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -0.54768, [ 3, -0.33333, -0.02915], [ 3, 0.46667, 0.04081]],
                        [ 0.10734, [ 3, -0.46667, -0.19834], [ 3, 0.36667, 0.15584]],
                        [ 0.51487, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 0.38048, [ 3, -0.43333, 0.01726], [ 3, 0.23333, -0.00930]],
                        [ 0.37119, [ 3, -0.23333, 0.00930], [ 3, 0.36667, -0.01461]],
                        [ -0.10472, [ 3, -0.36667, 0.13827], [ 3, 0.43333, -0.16341]],
                        [ -0.53387, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.5, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LShoulderPitch')
        times.append([0.2, 0.5, 0.8, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [2, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -0.02757, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -1.51146, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ -1.25025, [ 3, -0.46667, -0.26120], [ 3, 0.36667, 0.20523]],
                        [ 0.07206, [ 3, -0.36667, -0.38566], [ 3, 0.43333, 0.45578]],
                        [ 1.27409, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ 0.75573, [ 3, -0.23333, 0.00333], [ 3, 0.36667, -0.00524]],
                        [ 0.75049, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 1.29154, [ 3, -0.43333, -0.15226], [ 3, 0.36667, 0.12884]],
                        [ 1.2, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LShoulderRoll')
        times.append([0.3, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 1.55390, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 0.01683, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ 0.07666, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.07052, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 0.15643, [ 3, -0.43333, -0.08590], [ 3, 0.23333, 0.04626]],
                        [ 0.93899, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.67719, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 0.84648, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.2, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LElbowYaw')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ -2.07694, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -1.58006, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ -1.60461, [ 3, -0.46667, 0.02454], [ 3, 0.36667, -0.01928]],
                        [ -1.78715, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -1.32695, [ 3, -0.43333, -0.11683], [ 3, 0.23333, 0.06291]],
                        [ -1.24791, [ 3, -0.23333, -0.04593], [ 3, 0.36667, 0.07218]],
                        [ -0.97260, [ 3, -0.36667, -0.01072], [ 3, 0.43333, 0.01267]],
                        [ -0.95993, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LElbowRoll')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ -0.00873, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -0.35278, [ 3, -0.33333, 0.08741], [ 3, 0.46667, -0.12238]],
                        [ -0.63810, [ 3, -0.46667, 0.09306], [ 3, 0.36667, -0.07312]],
                        [ -0.85133, [ 3, -0.36667, 0.13944], [ 3, 0.43333, -0.16480]],
                        [ -1.55083, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ -0.73304, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.73653, [ 3, -0.36667, 0.00349], [ 3, 0.43333, -0.00413]],
                        [ -1.15506, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RShoulderPitch')
        times.append([0.2, 0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [2, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -0.02757, [ 3, -0.33333, 0.00000 ], [ 3, 0.33333, 0.00000]],
                        [ -1.51146, [ 3, -0.33333, 0.00000 ], [ 3, 0.46667, 0.00000]],
                        [ -1.22256, [ 3, -0.46667, -0.23805], [ 3, 0.36667, 0.18704]],
                        [ -0.23619, [ 3, -0.36667, -0.22007], [ 3, 0.43333, 0.26008]],
                        [ 0.21787, [ 3, -0.43333, -0.14857 ], [ 3, 0.23333, 0.08000]],
                        [ 0.44950, [ 3, -0.23333, -0.09028 ], [ 3, 0.36667, 0.14187]],
                        [ 0.91431, [ 3, -0.36667, -0.03894 ], [ 3, 0.43333, 0.04602]],
                        [ 0.96033, [ 3, -0.43333, -0.04602 ], [ 3, 0.36667, 0.03894]],
                        [ 1.2, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RShoulderRoll')
        times.append([0.3, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ -1.53558, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -0.19199, [ 3, -0.33333, -0.07793], [ 3, 0.46667, 0.10911]],
                        [ -0.08288, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.08288, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.22707, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ -0.18259, [ 3, -0.23333, -0.02831], [ 3, 0.36667, 0.04448]],
                        [ -0.00870, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.13197, [ 3, -0.43333, 0.01994], [ 3, 0.36667, -0.01687]],
                        [ -0.2, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RElbowYaw')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 2.07694, [ 3, -0.33333, 0.00000 ], [ 3, 0.33333, 0.00000]],
                        [ 1.56157, [ 3, -0.33333, 0.00000 ], [ 3, 0.46667, 0.00000]],
                        [ 1.61373, [ 3, -0.46667, -0.02319], [ 3, 0.36667, 0.01822]],
                        [ 1.68582, [ 3, -0.36667, -0.05296], [ 3, 0.43333, 0.06259]],
                        [ 1.96041, [ 3, -0.43333, 0.00000 ], [ 3, 0.23333, 0.00000]],
                        [ 1.95121, [ 3, -0.23333, 0.00920 ], [ 3, 0.36667, -0.01445]],
                        [ 0.66571, [ 3, -0.36667, 0.22845 ], [ 3, 0.43333, -0.26998]],
                        [ 0.39573, [ 3, -0.43333, 0.00000 ], [ 3, 0.36667, 0.00000]],
                        [ 0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RElbowRoll')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.10472, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 0.38201, [ 3, -0.33333, -0.07367], [ 3, 0.46667, 0.10313]],
                        [ 0.63512, [ 3, -0.46667, -0.21934], [ 3, 0.36667, 0.17234]],
                        [ 1.55705, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 0.00870, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ 0.00870, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.42343, [ 3, -0.36667, -0.09786], [ 3, 0.43333, 0.11566]],
                        [ 0.64926, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LHipYawPitch')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ -0.03371, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 0.03491, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ -0.43561, [ 3, -0.46667, 0.15197], [ 3, 0.36667, -0.11941]],
                        [ -0.77923, [ 3, -0.36667, 0.09257], [ 3, 0.43333, -0.10940]],
                        [ -1.04154, [ 3, -0.43333, 0.07932], [ 3, 0.23333, -0.04271]],
                        [ -1.530, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -1, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.56754, [ 3, -0.43333, -0.16414], [ 3, 0.36667, 0.13889]],
                        [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LHipRoll')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.06294, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ 0.00158, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.37732, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.29755, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ -0.29755, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.19486, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 0.12736, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LHipPitch')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.06140, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 0.00004, [ 3, -0.33333, 0.06136], [ 3, 0.46667, -0.08590]],
                        [ -1.56924, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -1.28085, [ 3, -0.36667, -0.08132], [ 3, 0.43333, 0.09611]],
                        [ -1.03694, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ -1.15966, [ 3, -0.23333, 0.01464], [ 3, 0.36667, -0.02301]],
                        [ -1.18267, [ 3, -0.36667, 0.01687], [ 3, 0.43333, -0.01994]],
                        [ -1.27011, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.4, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LKneePitch')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.12043, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 1.98968, [ 3, -0.33333, -0.08775], [ 3, 0.46667, 0.12285]],
                        [ 2.11253, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.28221, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 0.40493, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ 0.35738, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.71940, [ 3, -0.36667, -0.25311], [ 3, 0.43333, 0.29913]],
                        [ 2.01409, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.95, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LAnklePitch')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.92189, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -1.02974, [ 3, -0.33333, 0.08628], [ 3, 0.46667, -0.12080]],
                        [ -1.15054, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.21625, [ 3, -0.36667, -0.28428], [ 3, 0.43333, 0.33597]],
                        [ 0.71020, [ 3, -0.43333, -0.15307], [ 3, 0.23333, 0.08242]],
                        [ 0.92275, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.82525, [ 3, -0.36667, 0.09750], [ 3, 0.43333, -0.11522]],
                        [ -0.50166, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.55, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('LAnkleRoll')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ -0.00149, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 0.00004,  [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ -0.00149, [ 3, -0.46667, 0.00153], [ 3, 0.36667, -0.00121]],
                        [ -0.45249, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.30062, [ 3, -0.43333, -0.07246], [ 3, 0.23333, 0.03901]],
                        [ -0.11808, [ 3, -0.23333, -0.03361], [ 3, 0.36667, 0.05281]],
                        [ -0.04138, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.12114, [ 3, -0.43333, 0.01632], [ 3, 0.36667, -0.01381]],
                        [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RHipRoll')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.03142, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ 0.00158, [ 3, -0.46667, -0.00153], [ 3, 0.36667, 0.00121]],
                        [ 0.31144, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 0.25469, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ 0.32065, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.22707, [ 3, -0.36667, 0.06047], [ 3, 0.43333, -0.07146]],
                        [ -0.07512, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RHipPitch')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.07666, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -0.00004, [ 3, -0.33333, 0.07670], [ 3, 0.46667, -0.10738]],
                        [ -1.57699, [ 3, -0.46667, 0.10738], [ 3, 0.36667, -0.08437]],
                        [ -1.66136, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -1.19963, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ -1.59847, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.32218, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -0.71028, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.4, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RKneePitch')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ -0.07819, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 1.98968, [ 3, -0.33333, -0.06900], [ 3, 0.46667, 0.09660]],
                        [ 2.08628, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 1.74267, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 2.12019, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ 2.12019, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 2.12019, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 2.12019, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ 0.95, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RAnklePitch')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.92965, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ -1.02974, [ 3, -0.33333, 0.07746], [ 3, 0.46667, -0.10844]],
                        [ -1.13819, [ 3, -0.46667, 0.02925], [ 3, 0.36667, -0.02298]],
                        [ -1.18645, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -1.18645, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ -0.58901, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -1.18645, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ -1.18645, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.55, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

        names.append('RAnkleRoll')
        times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
        angles.append([ [ 0.18850, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                        [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                        [ 0.00618, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.00456, [ 3, -0.36667, 0.01074], [ 3, 0.43333, -0.01269]],
                        [ -0.09813, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                        [ -0.01376, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                        [ -0.09507, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                        [ 0.03532, [ 3, -0.43333, -0.02825], [ 3, 0.36667, 0.02390]],
                        [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        self.globals.motProxy.angleInterpolationBezier(names, times, angles)

    def cartesianRight( self, angle, x, y, interval1 = 0.1, interval2= 0.09, interval3 =0.09):
        """ Kick with angle and location as input """    
        
        # maxima input:
        # angle -> -0.3 to 0.5 (with x = 0.05, y =  0.00) 
        #          -0.1 to 0.7 (with x = 0.05, y =  0.03)
        #          -1.0        (with x = 0.05, y = -0.20 but do try -1.4, 0.0, -0.2 with the ball right next to nao) 
        #               to 0.1 (with x = 0.10, y = -0.08 though 0.3, -0.2, -0.08 has similar results)
        #          -0.2 to 0.5 (with x = 0.30, y =  0.00)
        
        if y > 0:
            angle = min( max( angle, -0.1), 0.7 )
            y = 0.03 if y > 0.03 else y
        elif y < -0.1:
            angle = min( max( angle, -1.0), 0.1 )
        if x > 0.2:
            angle = min( max( angle, -0.2), 0.5 )
        elif x < 0:
            x = 0
        if not -1 < angle < 1:
            angle = min( max( angle, -1 ), 1 )
            
        # move the torso above the standing leg for balance
        space = 2
        currentTorso = self.globals.motProxy.getPosition( 'Torso', space, True)          

        targetTorso  = [ 
        currentTorso[0] + 0.0, 
        currentTorso[1] + 0.04, 
        currentTorso[2] + 0.01, 
        currentTorso[3] + 0.0, 
        currentTorso[4] + 0.0, 
        currentTorso[5] + 0.0 ] 
        
        # current position in the world, used to calculate translation and rotation matrices
        currentRLeg = self.globals.motProxy.getPosition( 'RLeg', 1, True )
        
        self.globals.motProxy.setPosition( 'Torso', space, targetTorso, 0.8, almath.AXIS_MASK_ALL)
        time.sleep(0.4)
        # Balance on one leg, use arms for even more balance 
        self.globals.motProxy.setAngles(['RAnkleRoll', 'LAnkleRoll'], [0.325, 0.325], 0.1)
        self.globals.motProxy.setAngles(['RShoulderRoll', 'LShoulderRoll', 'LShoulderPitch', 'LElbowRoll', 'LElbowYaw'], [-0.4, 0.3 + 10 * y - angle, 0.5, -1.5, 0.3], 0.4)
        time.sleep(0.5)
        
        # convert target vectors to worldcoordinates 
        targets = list()
        z = currentRLeg[5]
        
        sz = math.sin(z) # used for rotation around the vertical z-axis
        cz = math.cos(z) # idem dito
        sa = math.sin(angle)
        ca = math.cos(angle)
        
        # ball is at position x,y,0.03. 
        # First step: Move leg backwards depending on the angle a. Default (a=0) gives x' = -0.15 + x, y' = y, z' = 0.1
        # (Note, to do this the vector has to be converted to worldcoordinates)
        targets.append( [ 
        currentRLeg[0] + ( x + 0.1 - 0.3 * ca ) * cz     + (-y + 0.3 * sa) * sz,
        currentRLeg[1] - ( ( x + 0.1 - 0.3 * ca ) * -sz  + (-y + 0.3 * sa) * cz ),
        currentRLeg[2] + 0.1, 
        currentRLeg[3] + 0.0, 
        currentRLeg[4] + 0.0, 
        currentRLeg[5] + minimizedAngle( angle ) ] ) 
        
        # Second step: Move leg towards the ball while respecting angle. Default (a=0) gives x'' = x, y'' = y, z'' = 0.03
        targets.append( [ # Note, -y because right y is negative. 
        currentRLeg[0] + ( x + 0.1 - 0.1 * ca ) * cz   + (-y +0.1 * sa) * sz,
        currentRLeg[1] - ( ( x + 0.1 - 0.1 * ca ) * -sz  + (-y  +0.1 * sa) * cz ),
        currentRLeg[2] + 0.0275, 
        currentRLeg[3] + 0.0, 
        currentRLeg[4] + 0.0, 
        currentRLeg[5] + minimizedAngle( angle ) ] )
        
        targets.append( [ # Note, -y because right y is negative. 
        currentRLeg[0] + 0.0,
        currentRLeg[1] + 0.0,
        currentRLeg[2] + 0.0175, 
        currentRLeg[3] + 0.0, 
        currentRLeg[4] + 0.0, 
        currentRLeg[5] + 0.0] )
                
        
        dur = 0.2 + abs(angle) * interval1 + abs(x) * interval2 + abs(y) * interval3 
        # move leg back
        self.globals.motProxy.setPosition( 'RLeg', 1, targets[0], 0.7, almath.AXIS_MASK_ALL )
        time.sleep(0.7)
        # simultaneously move arm back and leg forward
        self.globals.motProxy.setAngles('RShoulderPitch', 2, 0.9)
        
        self.globals.motProxy.positionInterpolation( 'RLeg', 1, targets[1], almath.AXIS_MASK_ALL, [dur], True)
        self.globals.motProxy.positionInterpolation( 'RLeg', 1, targets[2], almath.AXIS_MASK_ALL, [dur ], True)
        
        self.normalPose(True)
    """ Kick with angle and location as input """   
    def cartesianLeft( self, angle, x, y , interval1 = 0.0, interval2 = 0.1, interval3 = 0.1 ):
        #
        # maxima input:
        # angle -> -0.5 to 0.3 (with x = 0.05, y =  0.00) 
        #          -0.7 to 0.1 (with x = 0.05, y =  -0.03)
        #           1.0        (with x = 0.05, y = 0.20 but do try -1.4, 0.0, 0.2 with the ball right next to nao) 
        #              to -0.1 (with x = 0.10, y = 0.08 though -0.3, 0.2, 0.08 has similar results)
        #          -0.5 to 0.2 (with x = 0.30, y =  0.00)
        
        
        # Not safe to use with y > 0.1 or y < -0.03 or x > 0.15 or angle > 0.5 or -0.5
        
        if y < 0:
            angle = min( max( angle, -0.5), 0.1 )
            y = -0.02 if y < -0.02 else y
        elif y > -0.1:
            angle = min( max( angle, -0.1), 1.0 )
        if x > 0.2:
            angle = min( max( angle, -0.2), 0.2 )
        if x > 0.1:
            y = 0.1 if y > 0.1 else y
            y = -0.1 if y < -0.1 else y
        if not -1 < angle < 1:
            angle = min( max( angle, -1 ), 1 )
            
            
        # move the torso above the standing leg for balance
        space = 2
        currentTorso = self.globals.motProxy.getPosition( 'Torso', space, True)          

        targetTorso  = [ 
        currentTorso[0] + 0.0, 
        currentTorso[1] - 0.04, 
        currentTorso[2] + 0.01, 
        currentTorso[3] + 0.0, 
        currentTorso[4] + 0.0, 
        currentTorso[5] + 0.0 ] 
        
        # current position in the world, used to calculate translation and rotation matrices
        currentLLeg = self.globals.motProxy.getPosition( 'LLeg', 1, True )
        
        self.globals.motProxy.setPosition( 'Torso', space, targetTorso, 0.8, almath.AXIS_MASK_ALL)
        time.sleep(0.4)
        # Balance on one leg, use arms for even more balance 
        self.globals.motProxy.setAngles(['LAnkleRoll', 'RAnkleRoll'], [-0.325, -0.325], 0.1)
        self.globals.motProxy.setAngles(['LShoulderRoll', 'RShoulderRoll', 'RShoulderPitch', 'RElbowRoll', 'RElbowYaw'], [0.4, -0.3 - 10 * y + angle, 0.5, 1.5, 0.3], 0.4)
        time.sleep(0.5)
        
        # convert target vectors to worldcoordinates 
        targets = list()
        z = currentLLeg[5]
        
        sz = math.sin(z) # used for rotation around the vertical z-axis
        cz = math.cos(z) # idem dito
        sa = math.sin(angle)
        ca = math.cos(angle)
        
        # ball is at position x,y,0.03. 
        # First step: Move leg backwards depending on the angle a. Default (a=0) gives x' = -0.15 + x, y' = y, z' = 0.1
        # (Note, to do this the vector has to be converted to worldcoordinates)
        targets.append( [ 
        currentLLeg[0] + ( x + 0.1 - 0.3 * ca ) * cz     + (-y + 0.3 * sa) * sz,
        currentLLeg[1] - ( ( x + 0.1 - 0.3 * ca ) * -sz  + (-y + 0.3 * sa) * cz ),
        currentLLeg[2] + 0.1, 
        currentLLeg[3] + 0.0, 
        currentLLeg[4] + 0.0, 
        currentLLeg[5] + minimizedAngle( angle ) ] ) 
        
        # Second step: Move leg towards the ball while respecting angle. Default (a=0) gives x'' = x, y'' = y, z'' = 0.03
        targets.append( [ # Note, -y because right y is negative. 
        currentLLeg[0] + ( x + 0.1 - 0.1 * ca ) * cz   + (-y +0.1 * sa) * sz,
        currentLLeg[1] - ( ( x + 0.1 - 0.1 * ca ) * -sz  + (-y  +0.1 * sa) * cz ),
        currentLLeg[2] + 0.0275, 
        currentLLeg[3] + 0.0, 
        currentLLeg[4] + 0.0, 
        currentLLeg[5] + minimizedAngle( angle ) ] )
        
        targets.append( [ # Note, -y because right y is negative. 
        currentLLeg[0] + 0.0,
        currentLLeg[1] + 0.0,
        currentLLeg[2] + 0.0175, 
        currentLLeg[3] + 0.0, 
        currentLLeg[4] + 0.0, 
        currentLLeg[5] + 0.0] )
                
        
        dur = 0.2 + abs(angle) * interval1 + abs(x) * interval2 + abs(y) * interval3 
        # move leg back
        self.globals.motProxy.setPosition( 'LLeg', 1, targets[0], 0.7, almath.AXIS_MASK_ALL )
        time.sleep(0.7)
        # simultaneously move arm back and leg forward
        self.globals.motProxy.setAngles('LShoulderPitch', 2, 0.9)
        
        self.globals.motProxy.positionInterpolation( 'LLeg', 1, targets[1], almath.AXIS_MASK_ALL, [dur], True)
        self.globals.motProxy.positionInterpolation( 'LLeg', 1, targets[2], almath.AXIS_MASK_ALL, [dur ], True)
        
        self.normalPose(True)
        
    # non blocking call, relative
    def changeHead(self, yaw,pitch):
        self.globals.motProxy.changeAngles(['HeadYaw', 'HeadPitch'], [yaw, pitch], 0.3)

    # dive towards the left (keeper)   
    def diveLeft(self):
        names = list()
        angles = list()
        times = list()
        
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0.438], [-0.8], [2.11], [-1.186], [-0.09]])
        times.extend([[0.5], [0.5], [0.5], [0.5], [0.5]])
        
        names.append('LHipYawPitch')
        angles.append([0.1])
        times.append([0.5])
        
        names.extend(['RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[0.0], [-0.3], [0.6871], [-0.3099], [0.54788]])
        times.extend([[0.5], [0.5], [0.5], [0.5], [0.5]])

        self.globals.motProxy.post.angleInterpolation(names, angles, times, True)

        names = list()
        angles = list()

        names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])    
        angles.extend([-1.1,             0.5,            0.1883,    -0.5016] )

        names.extend(['RShoulderPitch','RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
        angles.extend([1.5,             0.3403,          0.1226,       0.903])

        self.globals.motProxy.angleInterpolationWithSpeed(names, angles, 1.0, True)    
        
        self.globals.motProxy.setStiffnesses('Body', 0)
        time.sleep(2)
        
        self.globals.motProxy.setStiffnesses('RArm', 0.8)
        self.globals.motProxy.setStiffnesses('LLeg', 0.6)
        self.globals.motProxy.setStiffnesses('RLeg', 0.6)
        
        # move arm around body to shift balance
        self.globals.motProxy.angleInterpolation(['RShoulderPitch','RShoulderRoll',   'RElbowYaw',     'RElbowRoll'], 
                                  [[1.372, 2.085],  [-1.2916, -0.105], [-0.154, -0.130],[1.1888, 0.380]], 
                                  [[0.4,   0.8],    [0.4,     0.8],    [0.4,    0.8],   [0.4,    0.8]], True)

        self.globals.motProxy.setAngles('RLeg', [-0.5,0,0,0.6,0.2,-0.2], 0.2)    
        self.globals.motProxy.setAngles('LLeg', [-0.5,0,0,0.6,0.2, 0.2], 0.2)
        self.globals.motProxy.setStiffnesses('RArm', 0)

        # wait until nao has taken a pose or three seconds have passed
        now = time.time()
        while self.globals.posProxy.getActualPoseAndTime()[0] != 'Back' and \
              self.globals.posProxy.getActualPoseAndTime()[0] != 'Belly' and \
              time.time() - now < 3.0 :
            pass
        
        self.globals.motProxy.setStiffnesses('Body',0.8)
        if self.globals.posProxy.getActualPoseAndTime()[0] == 'Back':
            self.backToStand()
            self.walkTo(0.1, 0.05, 1.5)

        elif self.globals.posProxy.getActualPoseAndTime()[0] == 'Belly':
            self.bellyToStand()
            self.walkTo(-0.1, -0.05, -1.5)
        else:
            print 'What the heck, I do not have a pose!'
            
    # dive towards the right (keeper)
    def diveRight(self):
        names = list()
        angles = list()
        times = list()
        
        names.extend(['RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[-0.438], [-0.8], [2.11], [-1.186], [0.09]])
        times.extend([[0.5], [0.5], [0.5], [0.5], [0.5]])
        
        names.append('LHipYawPitch')
        angles.append([0.1])
        times.append([0.5])
        
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0], [-0.3], [0.6871], [-0.3099], [-0.54788]])
        times.extend([[0.5], [0.5], [0.5], [0.5], [0.5]])

        self.globals.motProxy.post.angleInterpolation(names, angles, times, True)
        
        names = list()
        angles = list()
        
        names.extend(['RShoulderPitch','RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
        angles.extend([-1.1, -0.5, 0.1883, 0.5016])
        
        names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
        angles.extend([1.5, -0.3403, 0.1226, -0.903])

        self.globals.motProxy.angleInterpolationWithSpeed(names, angles, 1.0, True)
        
        self.globals.motProxy.setStiffnesses('Body', 0)

        time.sleep(2)

        self.globals.motProxy.setStiffnesses('LArm', 0.8)
        self.globals.motProxy.setStiffnesses('LLeg', 0.6)
        self.globals.motProxy.setStiffnesses('RLeg', 0.6)
        self.globals.motProxy.angleInterpolation(['LShoulderPitch','LShoulderRoll', 'LElbowYaw',      'LElbowRoll'], 
                                  [[1.372, 2.085],  [1.2916, 0.105], [-0.154, -0.130], [-1.1888, -0.380]], 
                                  [[0.4,   0.8],    [0.4,    0.8],   [0.4,    0.8],    [0.4,     0.8]], True)
        self.globals.motProxy.setAngles('LLeg', [-0.5,0,0,0.6,0.2, 0.2], 0.2)    
        self.globals.motProxy.setAngles('RLeg', [-0.5,0,0,0.6,0.2,-0.2], 0.2)
        self.globals.motProxy.setStiffnesses('RArm', 0)

        now = time.time()
        while self.globals.posProxy.getActualPoseAndTime()[0] != 'Back' and \
              self.globals.posProxy.getActualPoseAndTime()[0] != 'Belly' and \
              time.time() - now < 3.0:
            pass    
        self.globals.motProxy.setStiffnesses('Body',0.8)
        if self.globals.posProxy.getActualPoseAndTime()[0] == 'Back':
            self.backToStand()
            self.walkTo(0.1, -0.05, -1.5)
        elif self.globals.posProxy.getActualPoseAndTime()[0] == 'Belly':
            self.bellyToStand()
            self.walkTo(-0.1, 0.05, 1.5)
        else:
            print 'What the heck, I do not have a pose!'
            
    # heelball, not finished.
    def experimentalKick(self,angle):
        names = list()
        angles = list()
        times = list()
        
        names.extend(['RShoulderRoll', 'RShoulderPitch', 'LShoulderRoll', 'LShoulderPitch'])
        angles.extend([[-0.3],         [0.4],            [0.5],           [1.0]])
        times.extend([[0.5],           [0.5],            [0.5],           [0.5]])
        
        names.append('LHipYawPitch')
        angles.append([angle])
        times.append([1.2])

        names.extend(['RHipRoll', 'RHipPitch',             'RKneePitch',    'RAnklePitch',           'RAnkleRoll'])
        angles.extend([[0],       [-0.3, -1.2, -1.5], [1.0, 2.0, 1.2, 1.0], [-0.6, -1.2, 0.15, 0.3], [0.2]])
        times.extend([[0.5],      [0.5,   1.0,  1.5], [0.5, 1.0, 1.5, 2.0], [ 0.5,  1.0, 1.5,  2.0], [0.4]])    
        
        names.extend( ['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0],       [-0.4],      [0.95],        [-0.55],       [0.2]] )
        times.extend ([[0.5],     [ 0.4],      [ 0.4],        [0.4  ],       [0.4]] )
                        
        self.globals.motProxy.angleInterpolation(names, angles, times, True)
       

    # sidestep left (keeper)
    def footLeft(self):
        names = list()
        times = list()
        angles = list()

        names.extend( ['LShoulderPitch','LShoulderRoll','LElbowYaw','LElbowRoll','RShoulderPitch','RShoulderRoll'])
        angles.extend([[1.9],           [0.5],          [-0.3],     [-0.05],     [1.2],           [-0.43] ])
        times.extend( [[0.4],           [0.4],          [0.4],      [0.4],       [0.75],           [1.0  ] ])

        names.extend( ['RElbowYaw','RElbowRoll','LHipYawPitch','LHipRoll','LHipPitch','LKneePitch','LAnklePitch'])
        angles.extend([[-0.61],    [0.44],      [-0.98],       [0.68],     [-1.5,-1.1],[0.7, 0.0], [1.0, 2.0]])
        times.extend( [[ 0.75],    [0.75],      [0.6],         [0.75],     [0.75, 1.2],[0.75,1.2], [0.75, 1.2]])

        names.extend( ['LAnkleRoll', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'] )
        angles.extend([[-0.05],      [0.1426],   [-0.2222],   [2.11],       [-0.9],         [0.079]])
        times.extend( [[0.75],       [0.75],     [0.75],      [0.75],       [0.75],         [0.75]] )

        self.globals.motProxy.angleInterpolation(names, angles, times, True )
        
        # wait to stop the ball
        time.sleep(1)
        
        angles = list()
        times = list()
        
        '''
        converts an entire bodyAngleList from left- to right-oriented. 
        def function(input):
        allangle = list()
        for j in range(len(input)):
            oneangle = list()
            for i in range(len(input[0])):
                if i >= 2 and i <= 5:
                    if i == 3 or i == 5:
                        oneangle.append(-input[j][i+16])
                    else:
                        oneangle.append(input[j][i+16])
                elif i >= 6 and i <= 11:
                    if i == 7 or i == 11:
                        oneangle.append(-input[j][i+6])
                    else:
                        oneangle.append(input[j][i+6])
                elif i >= 12 and i <= 17:
                    if i == 13 or i == 17:
                        oneangle.append(-input[j][i-6])
                    else:
                        oneangle.append(input[j][i-6])
                elif i >= 18:
                    if i == 19 or i == 21:
                        oneangle.append(-input[j][i-16])
                    else:
                        oneangle.append(input[j][i-16])
                else:
                    oneangle.append(input[j][i])
            allangle.append(oneangle)
        return allangle
        '''
        
        anglelist = [ [0.056716039776802063, 0.31442803144454956, 1.9497560262680054,
                       0.4939899742603302, -0.30070596933364868, -0.09361596405506134,
                      -0.95717406272888184, 0.68565607070922852, -1.3116120100021362,
                       0.69034194946289063, 0.93200582265853882, -0.001575961709022522,
                      -0.95717406272888184, 0.14568804204463959, -0.24233004450798035,
                       2.112546443939209, -0.88209199905395508, 0.0076280385255813599,
                       1.3023240566253662, -0.33437004685401917, -0.61364197731018066,
                       0.42641004920005798],
                      [0.05825003981590271, 0.3159620463848114, 1.9497560262680054, 
                       0.50012600421905518, -0.29917198419570923, -0.090547963976860046, 
                      -0.96484404802322388, 0.68565607070922852, -1.5647220611572266, 
                       1.2747960090637207, 0.6535259485244751, -4.1961669921875e-05, 
                      -0.96484404802322388, 0.14568804204463959, -0.21165004372596741,
                       2.112546443939209, -0.90816998481750488, 0.0076280385255813599, 
                       1.3406740427017212, -0.33590406179428101, -0.61364197731018066, 
                       0.42487603425979614], 
                      [0.056716039776802063, 0.31442803144454956, 1.9359500408172607,
                       0.50012600421905518, -0.30070596933364868, -0.085945963859558105,
                      -0.97251403331756592, 0.68719005584716797, -1.5800620317459106,
                       1.4711480140686035, 0.45103797316551208, -0.18565596640110016,
                      -0.97251403331756592, 0.14568804204463959, -0.20858204364776611, 
                       2.112546443939209, -1.1229300498962402, 0.018366038799285889, 
                       1.4465200901031494, -0.33437004685401917, -0.61364197731018066, 
                       0.42487603425979614],
                      [0.056716039776802063, 0.3159620463848114, 1.9359500408172607,
                       0.50012600421905518, -0.30070596933364868, -0.084411963820457458,
                      -0.97251403331756592, 0.68719005584716797, -1.5800620317459106,
                       1.831637978553772, 0.1381019651889801, -0.19332596659660339,
                      -0.97251403331756592, 0.14262004196643829, -0.20704804360866547,
                       2.112546443939209, -1.132133960723877, -0.016915962100028992,
                       1.4557241201400757, -0.33437004685401917, -0.61364197731018066,
                       0.42487603425979614], 
                       [0.056716039776802063, 0.3159620463848114,
                       1.9328820705413818, 0.50012600421905518, -0.30070596933364868,
                      -0.084411963820457458, -0.98325204849243164, 0.68872404098510742,
                      -1.5754599571228027, 2.112546443939209, -0.22392204403877258,
                      -0.27616196870803833, -0.98325204849243164, 0.14415404200553894,
                      -0.20858204364776611, 2.112546443939209, -1.1894419193267822,
                       0.0045600384473800659, 1.4833360910415649, -0.33437004685401917,
                      -0.61057400703430176, 0.42487603425979614],
                      [0.064386039972305298, 0.3159620463848114, 1.9313479661941528,
                       0.47711598873138428, -0.29917198419570923, -0.085945963859558105,
                      -0.77616202831268311, 0.55066406726837158, -0.86521798372268677,
                       1.8837940692901611, -0.35431206226348877, -0.30837595462799072,
                      -0.77616202831268311,-0.1381019651889801, -0.3451080322265625, 
                       2.112546443939209, -1.1894419193267822, -0.10588795691728592,
                       1.6198620796203613, -0.33437004685401917, -0.61057400703430176, 
                       0.42487603425979614],
                      [0.065920040011405945, 0.31442803144454956, 1.9313479661941528,
                       0.47711598873138428, -0.29917198419570923, -0.085945963859558105,
                      -0.74855005741119385, 0.41107004880905151, -0.53540796041488647,
                       2.0755441188812256, -0.88047409057617188, -0.22553996741771698,
                      -0.74855005741119385, -0.16571396589279175, -0.37272006273269653,
                       2.112546443939209, -1.1894419193267822, -0.10435395687818527,
                       1.6290661096572876, -0.33437004685401917, -0.61057400703430176,
                       0.42487603425979614],
                      [0.059784039855003357, 0.30982604622840881, 1.925212025642395, 
                       0.4740479588508606, -0.29917198419570923, -0.085945963859558105, 
                      -0.75315207242965698, 0.40953606367111206,  -0.55381596088409424, 
                       2.1016221046447754, -0.92496007680892944, -0.16264596581459045, 
                      -0.75315207242965698, -0.17338396608829498, -0.38039004802703857,
                       2.112546443939209, -1.1894419193267822, -0.053731963038444519, 
                       1.6428720951080322, -0.32363206148147583, -0.60903996229171753,
                       0.42180806398391724], 
                      [0.078192040324211121, 0.31289404630661011, 1.0615699291229248,
                       0.81612998247146606, -0.055265963077545166, -0.75783801078796387,
                      -0.63656806945800781,0.25153404474258423, -0.22247196733951569,
                       1.7825499773025513, -0.77002608776092529, -0.27769595384597778, 
                      -0.63656806945800781, -0.45410597324371338, -0.47396403551101685, 
                       2.112546443939209, -1.1894419193267822, -0.050663962960243225, 
                       1.688892126083374, -0.32670003175735474, -0.4418339729309082,
                       0.034906584769487381],
                      [0.078192040324211121, 0.31289404630661011, 1.0631040334701538,
                       0.81612998247146606, -0.055265963077545166, -0.75937199592590332,
                      -0.69639408588409424, 0.081260040402412415, -0.05833396315574646,
                       1.5233039855957031, -0.63350003957748413, -0.30990996956825256,
                       -0.69639408588409424, -0.51853394508361816, -0.64423805475234985,
                       2.112546443939209, -1.1894419193267822, -0.10588795691728592,
                       1.6781541109085083, -0.32670003175735474, -0.44336795806884766,
                       0.034906584769487381],
                      [0.081260040402412415, 0.31289404630661011, 1.0723079442977905,
                       0.80999398231506348, -0.053731963038444519, -0.76243996620178223,
                      -0.60895603895187378, -0.14270396530628204, -0.1381019651889801,
                       1.7181220054626465, -1.101370096206665, -0.024585962295532227,
                      -0.60895603895187378, -0.5952339768409729, -0.78996807336807251,
                       2.112546443939209, -1.1894419193267822, -0.099751964211463928,
                       1.6996300220489502, -0.5966840386390686, -0.44796997308731079,
                       0.034906584769487381], 
                      [0.081260040402412415, 0.31289404630661011, 1.0738420486450195,
                       0.80999398231506348, -0.053731963038444519, -0.76243996620178223,
                      -0.31749606132507324, -0.37126997113227844, -0.50932997465133667, 
                       1.8500460386276245, -1.1335840225219727, 0.12574604153633118,
                      -0.31749606132507324, -0.45870798826217651, -0.81297802925109863, 
                       2.112546443939209, -1.1894419193267822, -0.10435395687818527, 
                       1.6996300220489502, -0.5966840386390686, -0.44796997308731079, 
                       0.034906584769487381], 
                      [0.081260040402412415, 0.31289404630661011, 1.0738420486450195, 
                       0.80999398231506348, -0.053731963038444519, -0.76243996620178223, 
                      -0.04291003942489624, -0.37126997113227844, -0.68573999404907227, 
                       1.8193659782409668, -1.0768260955810547, 0.12267804145812988, 
                      -0.04291003942489624, -0.28536596894264221, -0.83752202987670898, 
                       2.112546443939209, -1.1894419193267822, -0.092081964015960693, 
                       1.6996300220489502, -0.5966840386390686, -0.44796997308731079, 
                       0.034906584769487381]
                      ]
        for i in range(len(anglelist[0])):
                        # 1   2   3   4   5   6   7   8   9   10   11   12   13
            times.append([0.5, 1, 1.5, 2 ,2.5, 3, 3.5, 4, 4.3, 4.6, 4.9, 5.1,  5.5])
            
            oneangle = list()
            for j in range(len(anglelist)):
                oneangle.append(anglelist[j][i])
            angles.append(oneangle)
                        
        self.globals.motProxy.angleInterpolation('Body', angles, times, True)
       
        self.stance()

    # sidestep right (keeper)
    def footRight(self):
        names = list()
        times = list()
        angles = list()
        
        names = list()
        times = list()
        angles = list()

        names.extend( ['LShoulderPitch','LShoulderRoll','LElbowYaw','LElbowRoll','RShoulderPitch','RShoulderRoll'])
        angles.extend([[1.2],           [0.43],         [-0.61],    [-0.44],     [1.9],           [-0.5 ] ])
        times.extend( [[0.75],          [0.75],         [0.75],     [0.75],      [0.4],           [0.4  ] ])

        names.extend( ['RElbowYaw','RElbowRoll','LHipYawPitch','LHipRoll','LHipPitch','LKneePitch','LAnklePitch'])
        angles.extend([[-0.3 ],    [-0.05],     [-0.98],       [-0.1426], [-0.222],   [2.11],      [-0.9]])
        times.extend( [[ 0.4],     [0.4],       [0.6],         [0.75],    [0.75 ] ,   [0.75],      [0.75]])

        names.extend( ['LAnkleRoll', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'] )
        angles.extend([[-0.079],     [-0.68],    [-1.5,-1.1], [0.7, 0.0],   [1.0,  2.0],   [0.05]] )
        times.extend( [[0.75],       [0.75],     [0.75, 1.2], [0.75,1.2],   [0.75, 1.2],   [0.75]] )

        self.globals.motProxy.angleInterpolation(names, angles, times , True)
        
        # wait to stop the ball
        time.sleep(1)
        
        angles = list()
        times = list()
        
        anglelist = [[0.056716039776802063, 0.31442803144454956, 1.3023240566253662, 0.33437004685401917, 
                     -0.61364197731018066, -0.42641004920005798, -0.95717406272888184, -0.14568804204463959,
                     -0.24233004450798035, 2.112546443939209, -0.88209199905395508, -0.0076280385255813599, 
                      -0.95717406272888184, -0.68565607070922852, -1.3116120100021362, 0.69034194946289062,
                      0.93200582265853882, 0.001575961709022522, 1.9497560262680054, -0.4939899742603302, 
                      -0.30070596933364868, 0.09361596405506134],
                    [0.05825003981590271, 0.3159620463848114, 1.3406740427017212, 0.33590406179428101,
                     -0.61364197731018066, -0.42487603425979614, -0.96484404802322388, -0.14568804204463959,
                     -0.21165004372596741, 2.112546443939209, -0.90816998481750488, -0.0076280385255813599,
                     -0.96484404802322388, -0.68565607070922852, -1.5647220611572266, 1.2747960090637207,
                     0.6535259485244751, 4.1961669921875e-05, 1.9497560262680054, -0.50012600421905518,
                     -0.29917198419570923, 0.090547963976860046],
                    [0.056716039776802063, 0.31442803144454956, 1.4465200901031494, 0.33437004685401917,
                     -0.61364197731018066, -0.42487603425979614, -0.97251403331756592, -0.14568804204463959, -0.20858204364776611, 2.112546443939209, -1.1229300498962402, -0.018366038799285889, -0.97251403331756592, -0.68719005584716797, -1.5800620317459106, 1.4711480140686035, 0.45103797316551208, 0.18565596640110016, 1.9359500408172607, -0.50012600421905518, -0.30070596933364868, 0.085945963859558105],
                    [0.056716039776802063, 0.3159620463848114, 1.4557241201400757, 0.33437004685401917, -0.61364197731018066, -0.42487603425979614, -0.97251403331756592, -0.14262004196643829, -0.20704804360866547, 2.112546443939209, -1.132133960723877, 0.016915962100028992, -0.97251403331756592, -0.68719005584716797, -1.5800620317459106, 1.831637978553772, 0.1381019651889801, 0.19332596659660339, 1.9359500408172607, -0.50012600421905518, -0.30070596933364868, 0.084411963820457458],
                    [0.056716039776802063, 0.3159620463848114, 1.4833360910415649, 0.33437004685401917, -0.61057400703430176, -0.42487603425979614, -0.98325204849243164, -0.14415404200553894, -0.20858204364776611, 2.112546443939209, -1.1894419193267822, -0.0045600384473800659, -0.98325204849243164, -0.68872404098510742, -1.5754599571228027, 2.112546443939209, -0.22392204403877258, 0.27616196870803833, 1.9328820705413818, -0.50012600421905518, -0.30070596933364868, 0.084411963820457458],
                    [0.064386039972305298, 0.3159620463848114, 1.6198620796203613, 0.33437004685401917, -0.61057400703430176, -0.42487603425979614, -0.77616202831268311, 0.1381019651889801, -0.3451080322265625, 2.112546443939209, -1.1894419193267822, 0.10588795691728592, -0.77616202831268311, -0.55066406726837158, -0.86521798372268677, 1.8837940692901611, -0.35431206226348877, 0.30837595462799072, 1.9313479661941528, -0.47711598873138428, -0.29917198419570923, 0.085945963859558105],
                    [0.065920040011405945, 0.31442803144454956, 1.6290661096572876, 0.33437004685401917, -0.61057400703430176, -0.42487603425979614, -0.74855005741119385, 0.16571396589279175, -0.37272006273269653, 2.112546443939209, -1.1894419193267822, 0.10435395687818527, -0.74855005741119385, -0.41107004880905151, -0.53540796041488647, 2.0755441188812256, -0.88047409057617188, 0.22553996741771698, 1.9313479661941528, -0.47711598873138428, -0.29917198419570923, 0.085945963859558105],
                    [0.059784039855003357, 0.30982604622840881, 1.6428720951080322, 0.32363206148147583, -0.60903996229171753, -0.42180806398391724, -0.75315207242965698, 0.17338396608829498, -0.38039004802703857, 2.112546443939209, -1.1894419193267822, 0.053731963038444519, -0.75315207242965698, -0.40953606367111206, -0.55381596088409424, 2.1016221046447754, -0.92496007680892944, 0.16264596581459045, 1.925212025642395, -0.4740479588508606, -0.29917198419570923, 0.085945963859558105],
                    [0.078192040324211121, 0.31289404630661011, 1.688892126083374, 0.32670003175735474, -0.4418339729309082, -0.034906584769487381, -0.63656806945800781, 0.45410597324371338, -0.47396403551101685, 2.112546443939209, -1.1894419193267822, 0.050663962960243225, -0.63656806945800781, -0.25153404474258423, -0.22247196733951569, 1.7825499773025513, -0.77002608776092529, 0.27769595384597778, 1.0615699291229248, -0.81612998247146606, -0.055265963077545166, 0.75783801078796387],
                    [0.078192040324211121, 0.31289404630661011, 1.6781541109085083, 0.32670003175735474, -0.44336795806884766, -0.034906584769487381, -0.69639408588409424, 0.51853394508361816, -0.64423805475234985, 2.112546443939209, -1.1894419193267822, 0.10588795691728592, -0.69639408588409424, -0.081260040402412415, -0.05833396315574646, 1.5233039855957031, -0.63350003957748413, 0.30990996956825256, 1.0631040334701538, -0.81612998247146606, -0.055265963077545166, 0.75937199592590332],
                    [0.081260040402412415, 0.31289404630661011, 1.6996300220489502, 0.5966840386390686, -0.44796997308731079, -0.034906584769487381, -0.60895603895187378, 0.5952339768409729, -0.78996807336807251, 2.112546443939209, -1.1894419193267822, 0.099751964211463928, -0.60895603895187378, 0.14270396530628204, -0.1381019651889801, 1.7181220054626465, -1.101370096206665, 0.024585962295532227, 1.0723079442977905, -0.80999398231506348, -0.053731963038444519, 0.76243996620178223],
                    [0.081260040402412415, 0.31289404630661011, 1.6996300220489502, 0.5966840386390686, -0.44796997308731079, -0.034906584769487381, -0.31749606132507324, 0.45870798826217651, -0.81297802925109863, 2.112546443939209, -1.1894419193267822, 0.10435395687818527, -0.31749606132507324, 0.37126997113227844, -0.50932997465133667, 1.8500460386276245, -1.1335840225219727, -0.12574604153633118, 1.0738420486450195, -0.80999398231506348, -0.053731963038444519, 0.76243996620178223],
                    [0.081260040402412415, 0.31289404630661011, 1.6996300220489502, 0.5966840386390686, -0.44796997308731079, -0.034906584769487381, -0.04291003942489624, 0.28536596894264221, -0.83752202987670898, 2.112546443939209, -1.1894419193267822, 0.092081964015960693, -0.04291003942489624, 0.37126997113227844, -0.68573999404907227, 1.8193659782409668, -1.0768260955810547, -0.12267804145812988, 1.0738420486450195, -0.80999398231506348, -0.053731963038444519, 0.76243996620178223]]        
                    
        for i in range(len(anglelist[0])):
                        # 1   2   3   4   5   6   7   8   9   10   11   12   13
            times.append([0.5, 1, 1.5, 2 ,2.5, 3, 3.5, 4, 4.3, 4.6, 4.9, 5.1,  5.5])
            
            oneangle = list()
            for j in range(len(anglelist)):
                oneangle.append(anglelist[j][i])
            angles.append(oneangle)
            
                
        self.globals.motProxy.angleInterpolation('Body', angles, times, True)

        self.stance()    
        
    # return headposition [yaw, pitch]
    def getHeadPos(self, arg = True):
        return self.globals.motProxy.getAngles(['HeadYaw', 'HeadPitch'], arg)

    # return nao's current pose
    def getPose(self):
        return self.globals.posProxy.getActualPoseAndTime()[0]

    # return the x-, y-, rotational speed
    def getRobotVelocity(self):
        return self.globals.motProxy.getRobotVelocity()
                      
    # return if nao is walking
    def isWalking(self):
        return self.globals.motProxy.walkIsActive()

    # a normal pose for the keeper which prevents overheating (hopefully)    
    def keepNormalPose(self):
        anglelist = self.globals.motProxy.getAngles(['RHipPitch','RKneePitch', 'RAnklePitch'], True)
        if not( self.globals.posProxy.getActualPoseAndTime()[0] == 'Stand' 
                and -0.01 <= anglelist[0] <= 0.01 
                and -0.01 <= anglelist[1] <= 0.01 
                and -0.01 <= anglelist[2] <= 0.01 ):
            names = list()
            times = list()
            angles = list()
        
            names.extend( ['LShoulderPitch','LShoulderRoll','LElbowYaw','LElbowRoll','RShoulderPitch','RShoulderRoll'])
            angles.extend([[1.2],           [0.15],         [0.0],      [0.0],       [1.2],           [-0.15] ])
            times.extend( [[1.0],           [1.0],          [1.0],      [1.0],       [1.0],           [1.0  ] ])
     
            names.extend( ['RElbowYaw','RElbowRoll','LHipYawPitch','LHipRoll','LHipPitch','LKneePitch','LAnklePitch'])
            angles.extend([[0.0],      [0.0],       [0.0],         [0.0],     [0.0],       [0.0],      [0.0]])
            times.extend( [[1.0],      [1.0],       [1.0],         [1.0],     [1.1],       [1.1],      [1.1]])

            names.extend( ['LAnkleRoll', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'] )
            angles.extend([[0.0],        [0.0],      [0.0],       [0.0],        [0.0],         [0.0]] )
            times.extend( [[1.0],        [1.0],      [1.1],       [1.1],        [1.1],         [1.0]] )
            
            self.globals.motProxy.angleInterpolation(names, angles, times, True)    
                                    
    # kick towards front, right leg
    def kick(self, angle ):
        if angle >= 1.0:
            self.sideRightKick()
        elif angle >= 0:
            self.rKickAngled(angle )
        elif -1.0 <= angle < 0:
            self.lKickAngled( -angle )
        elif angle < -1.0:
            self.sideLeftKick()

    def kickOld(self, angle ):
        if angle >= 0.6:
            self.sideRightKickOld()
        elif angle >= 0:
            self.cartesianRightOld( angle, min( 0.04, max( coordinates[0], -0.2)), min ( max( coordinates[1], -0.1 ), 0.01 ) )            
        elif -0.6 <= angle < 0:
            self.cartesianLeftOld( angle, min( coordinates[0], 0.2), max ( min( coordinates[1], 0.1 ), -0.01 ) )
        elif angle <= -0.6:
            self.sideLeftKickOld()
    
    def kickStraight(self, angle):
        # angle slightly positive, kick towards left with rightleg
        if 0 <= angle < 0.2:
            names = ['RShoulderRoll', 'RShoulderPitch', 'LShoulderRoll', 'LShoulderPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', \
                     'RAnklePitch', 'RAnkleRoll', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll']
            angles = [[-0.3], [0.4], [0.5], [1.0], [0.0], [-0.4, -0.2], [0.95, 1.5], [-0.55, -1], [0.2], [0.0], [-0.4], [0.95], [-0.55], [0.2]]
            times =  [[ 0.5], [0.5], [0.5], [0.5], [0.5], [ 0.4,  0.8], [ 0.4, 0.8],  [0.4, 0.8], [0.4], [0.5], [ 0.4], [ 0.4], [ 0.4],  [0.4]]
            self.globals.motProxy.angleInterpolation(names, angles, times, True)
            
            self.globals.motProxy.angleInterpolationWithSpeed(['RShoulderPitch', 'RHipPitch', 'RKneePitch', 'RAnklePitch'], 
                                                 [1.5,               -0.7,        1.05,         -0.5],  
                                                 1.0 , True)
            
            self.globals.motProxy.angleInterpolation(['RHipPitch', 'RKneePitch', 'RAnklePitch'], \
                                        [-0.5,         1.1,        -0.65], 
                                        [[0.25],       [0.25],     [0.25]], True)
            self.normalPose(True)
            
        # kick towards front, left leg    
        elif -0.2 < angle < 0:  
            names = ['LShoulderRoll', 'LShoulderPitch', 'RShoulderRoll', 'RShoulderPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', \
                     'LAnkleRoll', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll']
            angles = [[0.3], [0.4], [-0.5], [1.0], [0.0], [-0.4, -0.2], [0.95, 1.5], [-0.55, -1], [-0.2], [0.0], [-0.4], [0.95], [-0.55], [-0.2]]
            times =  [[0.5], [0.5], [ 0.5], [0.5], [0.5], [ 0.4,  0.8], [ 0.4, 0.8], [ 0.4, 0.8], [ 0.4], [0.5], [ 0.4], [0.4] , [0.4],   [0.4]]        
            self.globals.motProxy.angleInterpolation(names, angles, times, True)
            self.globals.motProxy.angleInterpolationWithSpeed(['LShoulderPitch', 'LHipPitch', 'LKneePitch', 'LAnklePitch'],
                                                 [1.5,               -0.7,        1.05,         -0.5],        
                                                 1.0, True)
            self.globals.motProxy.angleInterpolation(['LHipPitch', 'LKneePitch', 'LAnklePitch'], 
                                        [-0.5,         1.1,          -0.65], 
                                        [[0.25],      [0.25],        [0.25]], True)    
            self.normalPose(True)
        
    # remove stiffness from body
    def kill(self):
        self.globals.motProxy.setStiffnesses('Body', 0)

    def killAll(self):
        self.globals.motProxy.killAll()
        
    # remove knee stiffness
    def killKnees(self):
        if self.globals.motProxy.getStiffnesses('RKneePitch')[0] > 0:
            self.globals.motProxy.post.stiffnessInterpolation(['RKneePitch', 'LKneePitch'], 
                                               [[0], [0]], [[0.15], [0.15]])
            self.globals.motProxy.angleInterpolation(['RHipPitch', 'LHipPitch'], 
                                      [[-1.1], [-1.1]], [[0.35],[0.35]], True)

    # stop walking if active    
    def killWalk(self, waitUntilKilled = True):
        if self.globals.motProxy.walkIsActive():
            if waitUntilKilled:
                self.walkTo(0,0,0.00001)
            else:
                self.postWalkTo( 0, 0, 0.0001) 
                
    # left kick with inputangle
    def lKickAngled(self, angle):
        self.globals.motProxy.angleInterpolationWithSpeed( \
            ["RAnklePitch", "RKneePitch", "LAnklePitch", "LKneePitch"],
            [-0.35,           0.6,          -0.35,        0.6],
            0.3,
            True)
        
        self.globals.motProxy.setAngles(['RShoulderRoll',    'LShoulderRoll'], #, 'LKneePitch', 'LAnklePitch'], 
                                 [-0.35 - 0.2*angle,  0.25,         ], 0.1)#    0.7,          -0.3], 0.1)
        time.sleep(1)
        # Left leg stretched, right leg goes backwards
        self.globals.motProxy.post.angleInterpolation(
            ['LHipYawPitch', 'RHipRoll',      'LHipRoll',            'RHipPitch',         'LHipPitch', 'LKneePitch',        'LAnklePitch'], 
            [[0.75*angle],   [-0.1-0.1*angle], [-0.075+0.295*angle], [-0.35 - 0.05*angle], [0.4],  [0.95, 0.5 - 0.45*angle],  [-0.6 + 0.1 * angle]],
            [[1.3],          [1.3],            [0.9],                   [1.7],               [1.0],   [0.4,  1.7],               [0.9]             ], 
            True)
        self.globals.motProxy.setAngles(['RShoulderPitch', 'RElbowRoll', 'RElbowYaw'], [0.3, -0.8, 0.3], 0.3 ) 
        time.sleep(2)
       # kick
        self.globals.motProxy.setAngles(['LShoulderPitch', 'LShoulderRoll'], [2, 0.35], 1)
        self.globals.motProxy.setAngles(['LHipYawPitch', 'RHipRoll', 'LHipPitch',     'LKneePitch',       'LAnklePitch'],
                                [0.75*angle,      -0.1,       -0.35-0.15*angle , 0.05 + 0.2*angle, 0.1 - 0.25*angle], 1)
        time.sleep(0.85)
        # return to start position
        self.globals.motProxy.post.angleInterpolation(
            ['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'LAnklePitch'],
            [[0],            [0],        [-0.4],      [0.95],        [0],       [-0.4],       [1.0],      [-0.6],       [0],         [-0.6]],
            [[0.65],         [0.85],     [0.85],      [0.85],       [0.85],     [0.85],       [0.85],      [0.65],        [0.6],     [ 0.85 ]], True)
        time.sleep(0.9)
        
    # a normal pose from which walking is almost immediately possible
    def normalPose(self, force = False): 
        anglelist = self.globals.motProxy.getAngles(['RHipPitch','RKneePitch', 'RAnklePitch'],True)
        if force or not( self.globals.posProxy.getActualPoseAndTime()[0] == 'Stand' and
                        -0.41 <= anglelist[0] <= -0.39 and
                        0.94 <= anglelist[1] <= 0.96 and 
                        -0.56 <= anglelist[2] <= -0.54):
            names = list()
            times = list()
            angles = list()
                    
            names.extend( ['LShoulderPitch','LShoulderRoll','LElbowYaw','LElbowRoll','RShoulderPitch','RShoulderRoll'])
            angles.extend([[1.2],           [0.15],         [0.0],      [0.0],       [1.2],           [-0.15] ])
            times.extend( [[1.0],           [1.0],          [1.0],      [1.0],       [1.0],           [1.0  ] ])
     
            names.extend( ['RElbowYaw','RElbowRoll','LHipYawPitch','LHipRoll','LHipPitch','LKneePitch','LAnklePitch'])
            angles.extend([[0.0],      [0.0],       [0.0],         [0.0],     [-0.4],      [0.95],     [-0.55]])
            times.extend( [[1.0],      [1.0],       [1.0],         [1.0],     [1.0],       [1.0],      [1.0]])

            names.extend( ['LAnkleRoll', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'] )
            angles.extend([[0.0],        [0.0],      [-0.4],      [0.95],       [-0.55],       [0.0]] )
            times.extend( [[1.0],        [1.0],      [1.0],       [1.0],        [1.0],         [1.0]] )

            self.globals.motProxy.angleInterpolation(names, angles, times, True)    
            
            
    # non-blocking walk call    
    def postWalkTo(self, x, y, angle):
        self.globals.motProxy.post.walkTo(x, y, angle,self.gaitConfig)
        
    # right kick with inputangle      
    def rKickAngled(self, angle):
        self.globals.motProxy.angleInterpolationWithSpeed( \
            ["LAnklePitch", "LKneePitch", "RAnklePitch", "RKneePitch"],
            [-0.35,           0.6,          -0.35,        0.6],
            0.3,
            True)
        
        self.globals.motProxy.setAngles(['LShoulderRoll',    'RShoulderRoll'], #, 'LKneePitch', 'LAnklePitch'], 
                                 [0.35 + 0.2*angle, -0.25,         ], 0.1)#    0.7,          -0.3], 0.1)
        time.sleep(1)
        # Left leg stretched, right leg goes backwards
        self.globals.motProxy.post.angleInterpolation(
            ['LHipYawPitch', 'LHipRoll',  'RHipRoll',          'LHipPitch',         'RHipPitch', 'RKneePitch',        'RAnklePitch'], 
            [[0.75*angle],   [0.1+0.1*angle], [0.075-0.295*angle], [-0.35 - 0.05*angle], [0.4],  [0.95, 0.5 - 0.45*angle],  [-0.6 + 0.1 * angle]],
            [[1.3],          [1.3],       [0.9],                   [1.7],               [1.0],   [0.4,  1.7],               [0.9]             ], 
            True)
        self.globals.motProxy.setAngles(['LShoulderPitch', 'LElbowRoll', 'LElbowYaw'], [0.3, -0.8, 0.3], 0.3 ) 
        time.sleep(2)
        # kick
        self.globals.motProxy.setAngles(['RShoulderPitch', 'RShoulderRoll'], [2, -0.35], 1)
        self.globals.motProxy.setAngles(['LHipYawPitch', 'LHipRoll', 'RHipPitch',     'RKneePitch',       'RAnklePitch'],
                                [0.75*angle,      0.1,       -0.35-0.2*angle , 0.05 + 0.2*angle, 0.1 - 0.25*angle], 1)
        time.sleep(0.85)
        # return to start position
        self.globals.motProxy.post.angleInterpolation(
            ['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'RAnklePitch', 'RAnkleRoll', 'LAnklePitch'],
            [[0],            [0],        [-0.4],      [1.0],        [0],       [-0.4],       [0.95],      [-0.6],       [0],         [-0.6]],
            [[0.65],         [0.85],     [0.85],      [0.85],       [0.85],     [0.85],       [0.85],      [0.65],        [0.6],     [ 0.85 ]], True)
        time.sleep(0.9)
        
    # non blocking call, absolute
    def setHead(self, yaw, pitch):
        self.globals.motProxy.setAngles(['HeadYaw', 'HeadPitch'], [yaw, pitch], 0.7)    

    # soft kick towards right, left leg
    def sideLeftKick(self):
        self.globals.motProxy.angleInterpolation(['RShoulderRoll', 'LShoulderRoll'], 
                                         [-0.4,             0.3], 
                                         [[0.4],           [0.4]], True)
        
        names = list()
        angles = list()
        times = list()
        
        names = ['RShoulderRoll','LHipRoll', 'LHipPitch', 'LKneePitch','LAnklePitch','RHipRoll','RHipPitch','RKneePitch']
        angles = [[-1],           [0,   0.45],[-0.4, -0.8],[1, 0.2],    [-0.55, 0.6], [0.05],   [-0.4],     [0.95]      ]
        times =  [[0.2],          [0.1, 1.8 ],[0.1, 1], [0.5, 1],     [0.5, 1],       [1.0],     [0.5],      [0.5]      ]
        
        self.globals.motProxy.post.angleInterpolation(names, angles, times, True)
        time.sleep(1.9)
        self.globals.motProxy.post.angleInterpolationWithSpeed(['LHipRoll', 'RShoulderRoll'], [-0.1, -0.1], 1.0, True)
        time.sleep(1.0)
        self.globals.motProxy.angleInterpolation(['LHipRoll','LHipPitch','LKneePitch','LAnklePitch'], 
                                         [[0.0],     [-0.6],     [1.3],       [-0.6]], 
                                         [[0.5],     [0.6],      [0.6],       [0.6]], True)
        time.sleep(0.6)
        
        # soft kick towards left, right leg
    # soft kick towards left, right leg
    def sideRightKick(self):
        self.globals.motProxy.angleInterpolation(['RShoulderRoll', 'LShoulderRoll'], 
                                         [ 0.4,           -0.3], 
                                         [[0.4],          [0.4]], True)
        
        names =  ['LShoulderRoll','RHipRoll','RHipPitch','RKneePitch','RAnklePitch','LHipRoll','LHipPitch','LKneePitch' ]
        angles = [[1],            [0,  -0.45],[-0.4, -0.8],[1, 0.2],[-0.55, 0.6],  [-0.05],   [-0.4],     [0.95]     ]
        times =  [[0.2],          [0.1, 1.8 ],[0.1, 1], [0.5, 1],     [0.5, 1],       [1.0],     [0.5],      [0.5]     ]
        
        self.globals.motProxy.post.angleInterpolation(names, angles, times, True)
        time.sleep(1.9)
        self.globals.motProxy.post.angleInterpolationWithSpeed(['RHipRoll', 'LShoulderRoll'], [0.1, 0.1], 1.0, True)
        time.sleep(1.0)
        self.globals.motProxy.post.angleInterpolation(['RHipRoll','RHipPitch', 'RKneePitch', 'RAnklePitch'], 
                                    [[0.0],     [-0.6],     [1.3],        [-0.6]], 
                                    [[0.5],     [0.6],       [0.6],        [0.6]], True)
        time.sleep(0.6)

    # keeper stance
    def stance(self):
        anglelist = self.globals.motProxy.getAngles(['RHipPitch','RKneePitch', 'RAnklePitch', 'LHipPitch', 'LKneePitch'],True)
        if not( -0.91 <= anglelist[0] <= 0.89 and 2.11 <= anglelist[1] <= 2.13 and 
                -1.21 <= anglelist[2] <= 1.21 and -0.91 <= anglelist[3] <= 0.89 and 2.11 <= anglelist[4] <= 2.13):
            names = list()
            angles = list()
            times = list()
            
            names.append('LLeg')
            angles.extend([[0], [0], [-0.9], [2.12], [-1.2], [0]])
            times.extend([[0.7], [0.7], [0.7], [0.7], [0.7], [0.7]])
            
            names.append('RLeg')
            angles.extend([[0],  [0.0], [-0.9], [2.12], [-1.2], [0]  ])
            times.extend([[0.7], [0.7], [ 0.7], [0.70],    [0.7],     [0.7]])
            
            names.append('RArm')
            angles.extend([[1.2], [-0.1], [0], [0]])
            times.extend([ [0.7], [0.7], [0.7], [0.7]])

            names.append('LArm')
            angles.extend([[1.2], [0.1], [0],  [0]])
            times.extend([[0.7], [0.7], [0.7], [0.7]])
            
            self.globals.motProxy.post.angleInterpolation(names, angles, times, True)

    # stand up if fallen down, return fallen==True
    def standUp(self):
        fallen = False
        pose = self.getPose()
        if pose == 'Back':
            
            self.stiff()
            self.backToStand()
            fallen = True
            
        elif pose == 'Belly':
            
            self.stiff()
            self.bellyToStand()
            fallen = True
    
        return fallen

    # activate stiffness
    def stiff(self):
        if self.globals.motProxy.getStiffnesses('HeadPitch') != 0:
            self.globals.motProxy.setStiffnesses(['RArm', 'LArm', 'LLeg', 'RLeg', 'Head'],
            [0.6, 0.6, 0.6, 0.6,0.6,0.6,0.6,0.6, 
             0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 
             0.95, 0.95, 0.95,0.95,0.95,0.95, 0.6,0.6])
        
    # set stiffness for knees again
    def stiffKnees(self):
        if self.globals.motProxy.getStiffnesses('RKneePitch')[0] < 0.95:
            self.globals.motProxy.post.stiffnessInterpolation(['RKneePitch', 'LKneePitch'], 
                                               [[0.95], [0.95]], [[0.15], [0.15]])
            self.globals.motProxy.angleInterpolation(['RHipPitch', 'LHipPitch'], 
                                      [[-1.0], [-1.0]], [[0.35],[0.35]], True)
            

        self.globals.motProxy.setStiffnesses(['RKneePitch','LKneePitch','RAnklePitch','LAnklePitch'], 0.95)
        while self.globals.motProxy.getStiffnesses ('RKneePitch') < 0.95:
            pass


        if self.globals.motProxy.getStiffnesses('RKneePitch')[0] < 0.95:
            self.globals.motProxy.post.stiffnessInterpolation(['RKneePitch', 'LKneePitch'], 
                                               [[0.95], [0.95]], [[0.05], [0.05]])
            self.globals.motProxy.angleInterpolation(['RHipPitch', 'LHipPitch'], 
                                      [[-1.0], [-1.0]], [[0.15],[0.15]], True)

    # footstepplanner                                  
    def setFootSteps( self, legName, footSteps, timeList, clearExisting = True ):
        #legName = ["LLeg", "RLeg"]
        #X       = 0.2
        #Y       = 0.1
        #Theta   = 0.3
        #footSteps = [[X, Y, Theta], [X, -Y, Theta]]
        #timeList = [0.6, 1.2]
        #clearExisting = False
        self.globals.motProxy.setFootSteps(legName, footSteps, timeList, clearExisting)
                                          
    # setWalkTargetVelocity function as specified in documentation (with check for valid parameters)
    def setWalkTargetVelocity(self,x,y,t,f):
        x = float( x )
        y = float( y )
        t = float( t )
        self.globals.motProxy.setWalkTargetVelocity(x,y,t,f,self.gaitConfig)
        
    # blocking walk call
    def walkTo(self, x,y,angle):
        self.globals.motProxy.walkTo(x,y,angle,self.gaitConfig)

    def cartesianRightOld( self, angle, x,y , interval1 = 0.1, interval2= 0.09, interval3 =0.09):
        
        # maxima input:
        # angle -> -0.3 to 0.5 (with x = 0.05, y =  0.00) 
        #          -0.1 to 0.7 (with x = 0.05, y =  0.03)
        #          -1.0        (with x = 0.05, y = -0.20 but do try -1.4, 0.0, -0.2 with the ball right next to nao) 
        #               to 0.1 (with x = 0.10, y = -0.08 though 0.3, -0.2, -0.08 has similar results)
        #          -0.2 to 0.5 (with x = 0.30, y =  0.00)
        
        if y > 0:
            angle = min( max( angle, -0.1), 0.7 )
            y = 0.03 if y > 0.03 else y
        elif y < -0.1:
            angle = min( max( angle, -1.0), 0.1 )
        if x > 0.2:
            angle = min( max( angle, -0.2), 0.5 )
        elif x < 0:
            x = 0
        if not -1 < angle < 1:
            angle = min( max( angle, -1 ), 1 )
            
        # move the torso above the standing leg for balance
        space = 2
        currentTorso = self.globals.motProxy.getPosition( 'Torso', space, True)          

        targetTorso  = [ 
        currentTorso[0] + 0.0, 
        currentTorso[1] + 0.04, 
        currentTorso[2] + 0.01, 
        currentTorso[3] + 0.0, 
        currentTorso[4] + 0.0, 
        currentTorso[5] + 0.0 ] 
        
        # current position in the world, used to calculate translation and rotation matrices
        currentRLeg = self.globals.motProxy.getPosition( 'RLeg', 1, True )
        
        self.globals.motProxy.setPosition( 'Torso', space, targetTorso, 0.8, almath.AXIS_MASK_ALL)
        time.sleep(0.4)
        # Balance on one leg, use arms for even more balance 
        self.globals.motProxy.setAngles(['RAnkleRoll', 'LAnkleRoll'], [0.325, 0.325], 0.1)
        self.globals.motProxy.setAngles(['RShoulderRoll', 'LShoulderRoll', 'LShoulderPitch', 'LElbowRoll', 'LElbowYaw'], [-0.4, 0.3 + 10 * y - angle, 0.5, -1.5, 0.3], 0.4)
        time.sleep(0.5)
        
        # convert target vectors to worldcoordinates 
        targets = list()
        z = currentRLeg[5]
        
        sz = math.sin(z) # used for rotation around the vertical z-axis
        cz = math.cos(z) # idem dito
        sa = math.sin(angle)
        ca = math.cos(angle)
        
        # ball is at position x,y,0.03. 
        # First step: Move leg backwards depending on the angle a. Default (a=0) gives x' = -0.15 + x, y' = y, z' = 0.1
        # (Note, to do this the vector has to be converted to worldcoordinates)
        targets.append( [ 
        currentRLeg[0] + ( x + 0.1 - 0.3 * ca ) * cz     + (-y + 0.3 * sa) * sz,
        currentRLeg[1] - ( ( x + 0.1 - 0.3 * ca ) * -sz  + (-y + 0.3 * sa) * cz ),
        currentRLeg[2] + 0.1, 
        currentRLeg[3] + 0.0, 
        currentRLeg[4] + 0.0, 
        currentRLeg[5] + minimizedAngle( angle ) ] ) 
        
        # Second step: Move leg towards the ball while respecting angle. Default (a=0) gives x'' = x, y'' = y, z'' = 0.03
        targets.append( [ # Note, -y because right y is negative. 
        currentRLeg[0] + ( x + 0.1 - 0.1 * ca ) * cz   + (-y +0.1 * sa) * sz,
        currentRLeg[1] - ( ( x + 0.1 - 0.1 * ca ) * -sz  + (-y  +0.1 * sa) * cz ),
        currentRLeg[2] + 0.0275, 
        currentRLeg[3] + 0.0, 
        currentRLeg[4] + 0.0, 
        currentRLeg[5] + minimizedAngle( angle ) ] )
        
        targets.append( [ # Note, -y because right y is negative. 
        currentRLeg[0] + 0.0,
        currentRLeg[1] + 0.0,
        currentRLeg[2] + 0.0175, 
        currentRLeg[3] + 0.0, 
        currentRLeg[4] + 0.0, 
        currentRLeg[5] + 0.0] )
                
        
        dur = 0.2 + abs(angle) * interval1 + abs(x) * interval2 + abs(y) * interval3 
        # move leg back
        self.globals.motProxy.setPosition( 'RLeg', 1, targets[0], 0.7, almath.AXIS_MASK_ALL )
        time.sleep(0.7)
        # simultaneously move arm back and leg forward
        self.globals.motProxy.setAngles('RShoulderPitch', 2, 0.9)
        
        self.globals.motProxy.positionInterpolation( 'RLeg', 1, targets[1], almath.AXIS_MASK_ALL, [dur], True)
        self.globals.motProxy.positionInterpolation( 'RLeg', 1, targets[2], almath.AXIS_MASK_ALL, [dur ], True)
        
        self.normalPose(True)
    """ Kick with angle and location as input """   
    def cartesianLeftOld( self, angle, x, y , interval1 = 0.0, interval2 = 0.1, interval3 = 0.1 ):
        #
        # maxima input:
        # angle -> -0.5 to 0.3 (with x = 0.05, y =  0.00) 
        #          -0.7 to 0.1 (with x = 0.05, y =  -0.03)
        #           1.0        (with x = 0.05, y = 0.20 but do try -1.4, 0.0, 0.2 with the ball right next to nao) 
        #              to -0.1 (with x = 0.10, y = 0.08 though -0.3, 0.2, 0.08 has similar results)
        #          -0.5 to 0.2 (with x = 0.30, y =  0.00)
        
        
        # Not safe to use with y > 0.1 or y < -0.03 or x > 0.15 or angle > 0.5 or -0.5
        
        if y < 0:
            angle = min( max( angle, -0.5), 0.1 )
            y = -0.02 if y < -0.02 else y
        elif y > -0.1:
            angle = min( max( angle, -0.1), 1.0 )
        if x > 0.2:
            angle = min( max( angle, -0.2), 0.2 )
        if x > 0.1:
            y = 0.1 if y > 0.1 else y
            y = -0.1 if y < -0.1 else y
        if not -1 < angle < 1:
            angle = min( max( angle, -1 ), 1 )
            
            
        # move the torso above the standing leg for balance
        space = 2
        currentTorso = self.globals.motProxy.getPosition( 'Torso', space, True)          

        targetTorso  = [ 
        currentTorso[0] + 0.0, 
        currentTorso[1] - 0.04, 
        currentTorso[2] + 0.01, 
        currentTorso[3] + 0.0, 
        currentTorso[4] + 0.0, 
        currentTorso[5] + 0.0 ] 
        
        # current position in the world, used to calculate translation and rotation matrices
        currentLLeg = self.globals.motProxy.getPosition( 'LLeg', 1, True )
        
        self.globals.motProxy.setPosition( 'Torso', space, targetTorso, 0.8, almath.AXIS_MASK_ALL)
        time.sleep(0.4)
        # Balance on one leg, use arms for even more balance 
        self.globals.motProxy.setAngles(['LAnkleRoll', 'RAnkleRoll'], [-0.325, -0.325], 0.1)
        self.globals.motProxy.setAngles(['LShoulderRoll', 'RShoulderRoll', 'RShoulderPitch', 'RElbowRoll', 'RElbowYaw'], [0.4, -0.3 - 10 * y + angle, 0.5, 1.5, 0.3], 0.4)
        time.sleep(0.5)
        
        # convert target vectors to worldcoordinates 
        targets = list()
        z = currentLLeg[5]
        
        sz = math.sin(z) # used for rotation around the vertical z-axis
        cz = math.cos(z) # idem dito
        sa = math.sin(angle)
        ca = math.cos(angle)
        
        # ball is at position x,y,0.03. 
        # First step: Move leg backwards depending on the angle a. Default (a=0) gives x' = -0.15 + x, y' = y, z' = 0.1
        # (Note, to do this the vector has to be converted to worldcoordinates)
        targets.append( [ 
        currentLLeg[0] + ( x + 0.1 - 0.3 * ca ) * cz     + (-y + 0.3 * sa) * sz,
        currentLLeg[1] - ( ( x + 0.1 - 0.3 * ca ) * -sz  + (-y + 0.3 * sa) * cz ),
        currentLLeg[2] + 0.1, 
        currentLLeg[3] + 0.0, 
        currentLLeg[4] + 0.0, 
        currentLLeg[5] + minimizedAngle( angle ) ] ) 
        
        # Second step: Move leg towards the ball while respecting angle. Default (a=0) gives x'' = x, y'' = y, z'' = 0.03
        targets.append( [ # Note, -y because right y is negative. 
        currentLLeg[0] + ( x + 0.1 - 0.1 * ca ) * cz   + (-y +0.1 * sa) * sz,
        currentLLeg[1] - ( ( x + 0.1 - 0.1 * ca ) * -sz  + (-y  +0.1 * sa) * cz ),
        currentLLeg[2] + 0.0275, 
        currentLLeg[3] + 0.0, 
        currentLLeg[4] + 0.0, 
        currentLLeg[5] + minimizedAngle( angle ) ] )
        
        targets.append( [ # Note, -y because right y is negative. 
        currentLLeg[0] + 0.0,
        currentLLeg[1] + 0.0,
        currentLLeg[2] + 0.0175, 
        currentLLeg[3] + 0.0, 
        currentLLeg[4] + 0.0, 
        currentLLeg[5] + 0.0] )
                
        
        dur = 0.2 + abs(angle) * interval1 + abs(x) * interval2 + abs(y) * interval3 
        # move leg back
        self.globals.motProxy.setPosition( 'LLeg', 1, targets[0], 0.7, almath.AXIS_MASK_ALL )
        time.sleep(0.7)
        # simultaneously move arm back and leg forward
        self.globals.motProxy.setAngles('LShoulderPitch', 2, 0.9)
        
        self.globals.motProxy.positionInterpolation( 'LLeg', 1, targets[1], almath.AXIS_MASK_ALL, [dur], True)
        self.globals.motProxy.positionInterpolation( 'LLeg', 1, targets[2], almath.AXIS_MASK_ALL, [dur ], True)
        
        self.normalPose(True)
