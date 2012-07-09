# @file mframework.py
# @func main-framework module. 
#       Handles module-dictionary and starts system
#       Is called by config.py
# @auth Hessel van der Molen
#       hmolen.science@gmail.com
# @date 4 may 2012
import os, sys

#@func: listFiles(dir)
#@       Adds recursively all paths of dirs in given directory
#@para: 'dir'               - full path to directory which has to be imported
def listFiles(dir):
    sys.path.append(dir)
    subdirlist = []
    for item in os.listdir(dir):
        founditem = os.path.join(dir,item)
        if not os.path.isfile(founditem):
            subdirlist.append(founditem)
        for subdir in subdirlist:
            listFiles(subdir) 


#@func: startUpFramework(moduledictionary, VERBOSE)
#        Starts framework, loads modules and starts main system file
#@para: 'moduledictionary' - dictionary containing modules (from config.py)
#@para: 'VERBOSE'            - print framework process
def startUpFramework(moduledictionary, VERBOSE):
    moduledir = os.path.join(os.getcwd(), "modules")
    listFiles(moduledir)
    
    #import module-handles
    import mloader as loader
    modules = loader.mLoader()  #get module-class
    
    #load modules
    r = modules.loadModules(moduledictionary, VERBOSE)

    if (r == 1):
        #set dependencies
        r = modules.setDependencies(VERBOSE)

        if (r == 1):
            #start main-module
            if (VERBOSE): print "Starting system..."
            modules.getMainModule().start()
            
            if (VERBOSE): print "System finished..."

    if (VERBOSE):
        if (r != 1):      
            print "An error occured during framework initialization"
            print "Framework terminiated"
        else:
            print "Framework terminiated succesfully"
