# @file mloader.py
# @func Loads & maintains modules
#       Is called by mframework.py
# @auth Hessel van der Molen
#       hmolen.science@gmail.com
# @date 4 may 2012

class mLoader():
    #privat variables
    __moduledict = {}
    __mainmodule = None
    
    # builds module dictionary
    def loadModules(self, moduledict, VERBOSE):
        for i in moduledict:
            if (i == "main"):   #-> mainmodule
                #import module
                mainModName = moduledict[i]
                module = self.importModule(mainModName)
                #test start-function
                if not hasattr(module, "start"):
                    print '\n' + "Error: (loadModules) Main-Module '" + str(mainModName) + "' does not contain a 'start'-function"  
                    exit()
                else:
                    #put module in 'mainmodule' and 'moduledict'
                    self.__mainmodule = module
                    self.__moduledict["main"] = module
                    if (VERBOSE): print "Main-Module loaded: '" + str(mainModName) + "' as 'main'."
            elif moduledict[i][0] == 1:
                #import module
                modName = moduledict[i][1]
                module = self.importModule(modName)
                #put module in 'moduledict'
                self.__moduledict[i] = module
                if (VERBOSE): print "Module '" + str(modName) + "' loaded as '" + str(i) +  "'."
            else:
                if (VERBOSE): print "Module '" + str(i) + "' not loaded."
                
        #return true
        return 1
    
    #import module
    def importModule(self, name):        
        #import handling
        try:
            m = __import__(name)
        except ImportError, ee:
            print '\n>> ' + str(ee)
            print "Error: (importModule) module '" + name + "' does not exist."
            exit()        
        except SyntaxError, ee: 
            print '\n>> ' + str(ee)
            print "Error: (importModule) module '" + name + "' has syntax error."
            exit()
            
        #class handling
        try:
            constructor = getattr(m, name)
        except AttributeError, ee:
            print '\n>> ' + str(ee)
            print "Error: (importModule) module '" + name + "' does not has the correct classname"
            exit()
        
        #create module
        module = constructor()
        return module
    
    def setDependencies(self, VERBOSE):
        try:
            for m in self.__moduledict:
                if (VERBOSE): print "Setting dependencies for module '" + str(m) + "'..."
                self.__moduledict[m].setDependencies(self)
            #return true    
            return 1
        except Exception, ee:
            print '\n>> ' + str(ee)
            print "Error: (setDependencies) problem while loading dependencies of module '" + m + "'"
            exit()
    
    #return list with the names loaded modules (strings)
    def getModules(self):
        return self.__moduledict.keys()
    
    #return pointer to module with name <module>
    def getModule(self, module):
        try:
            return self.__moduledict[module]
        except Exception, ee:
            print '\n' + "Error: (getModule) Module '" +  module + "' cannot be used, it is not loaded."
            exit()
    
    #return pointer to module with name <module> or (if not loaded) return None
    def getModuleNone(self, module):
        if (module in self.__moduledict):
            return self.__moduledict[module]
        else:
            return None
            
    #return true if module <module> is loaded in dictionary
    def isLoaded(self, module):
        return module in self.__moduledict
        
    #return pointer to the main module
    def getMainModule(self):
        return self.__mainmodule