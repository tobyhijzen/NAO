FRAMEWORK USAGE README v2.0 - 7 july 2012
Hessel van der Molen - hmolen.science@gmail.com

WHAT IT DOES:
----------------------
The presented framework is able to load multiple modules
It consists of a simple config-file in which modules are registrated and loaded.
Modules have to be stored in the 'modules' folder, found in the same directory as this readme.
Since the framework checks all folders in the modules folder, modules can be placed in any subdirectory.

To start the system and run your own code, run 'config.py'
----------------------


CONFIG.PY
----------------------
Contains a dictionairy of all modules.

A module is loaded using the following syntax:
    >> moduledict["<module-system-reference-name>"] = [<load>, "<class-name-of-module>"]
<load> = 0 or 1, depending if the module has to be loaded (1) or not (0).

A special module is the main module. This module is the main file of your program.
Loading a main module is done using the following syntax:
    >> moduledict["main"]                           = "<class-name-of-module>"
----------------------


MODULE
----------------------
A module is a file in which a single class is defined. 
The name of the class should be equal to the name of the file.

The specified module should contain at least a function called 'setDependencies(modules)'
This function is used to import other loaded modules in the current module. 
Loading other modules in this function is done using one of the following commands:

    #return list with the names of loaded modules (strings)
    >> modulelist = modules.getModules()

    #return pointer to the main module
    >> modules.getMainModule()
         
    #return true if module is loaded in dictionary
    >> modules.isLoaded("<module-system-reference-name>")

    #return pointer to module, or throw error if module is not loaded
    >> modules.getModule("<module-system-reference-name>")

    #return pointer to module, or (if not loaded) return None
    >> modules.getModuleNone("<module-system-reference-name>")
   
The returned module-pointer can be stored in a variable. 
A function (or variable) from the loaded module can be accesed using 'normal' python coding:
    >> <variable-containing_pointer>.<function>()
----------------------


MAIN-MODULE
----------------------
The main module is a special module. This module should (besides the 'setDependencies(modules)'-function)
contain a function called 'start()'. 

After all modules are loaded by the framework, this function is called. The 'start()' function starts the
user defined program.

Just as with 'normal' modules, the class-name of the main module should equal its file-name.
----------------------


EXTRA NOTES
----------------------
Each module is only included once, which has some influence on the behaviour of the system:

Lets assume that there are two modules, called "foo1" and "foo2".
Both modules are dependent on module "bar" (dependency is set by 'setDependencies(modules)').
If "foo1" calls "bar" and adjusts some values in the module, these values also change for "foo2":

    bar.data = 'data1'
    
    foo1 calls 'bar.getData()'
            --> return is "data1"
    foo2 calls 'bar.getData()'
            --> return is "data1"
            
    foo2 calls 'bar.setData("data2")

    foo1 calls 'bar.getData()'
            --> return is "data2"
    foo2 calls 'bar.getData()'
            --> return is "data2"   

With other words: each dependency shares the exact same reference to a module.
----------------------