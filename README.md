# Water ripple effect and seabed distortion

Below GIF is made with PygameShader (GPU shader ==> wave_gpu method). Wave_gpu method is the cython method developped in this
github page ported to CUDA for higher resolutions and better perforamces.
For a full demo install PygameShader and run the demo PygameShader/Demo/GPU_demo_ripple.py 

PS refers to the dependencies section (CUDA must be installed). 


<p align="center">
    <img src="https://github.com/yoyoberenguer/Water-Ripple-Effect/blob/master/ripples.gif?raw=true">
</p>

## Demo 
For a full demo, please click on the new release version 1.0.2 as shown below
<p align="left">
    <img src="https://github.com/yoyoberenguer/Water-Ripple-Effect/blob/master/Assets/Capture2.PNG?raw=true">
</p>

Click on the executable setup_RippleEffect.exe to download the setup file and run it onto your machine, 
The installation process might be flagged as unsafe by you anti-virus. 

<p align="left">
    <img src="https://github.com/yoyoberenguer/Water-Ripple-Effect/blob/master/Assets/Capture1.PNG?raw=true">
</p>


## New version

The most recent versions of the below algorithms are now integrated within the project PygameShader, 
and will be updated from from that project only.
- Water ripple effect and seabed distortion (GPU)
- Surface water ripple effect (CPU method)


## Methods

This github page contains 3 different rendering methods.

1) Pure Python 
2) Cython Version 
3) OpenMP Version (Multi-processing)


## Pure Python ver 3.6 - 3.9

In the pure python method I am using two different techniques

1. Iterating method 

   Description : Iterating over all pixels values width x height and performing a blur on 
   adjacent pixels  
   performance result: Slow method and not usable for real time rendering for screen 
   resolution above 100 x 100 pixels!. Python version 3.11 might provide better performances

2. Numpy arrays

   Description : Instead of going through all the pixels inside a loop and applying 
   a blur for each pixels, the technique is to call separately the method numpy.roll for every 
   directions (up, down, left, right) and sum all 4 numpy arrays. This provides the
   equivalent of blur effect for each pixels in only 4 operations. 
   
   pixels             | numpy                            |   convolution direction 
   -------------------|----------------------------------|------------------------
   (x, y + 1)         | numpy.roll(previous, +1, axis=0) |    down pass
   (x, y - 1)         | numpy.roll(previous, -1, axis=0) |    up pass
   (x + 1, y)         | numpy.roll(previous, -1, axis=1) |    left pass
   (x - 1, y)         | numpy.roll(previous, +1, axis=1) |    right pass

   performance Result : Using numpy array is 300 times faster than the pure python version, however this
   method is still not adequate for a real time rendering.  
   


## Cython and OpenMP rendering     


The Cython version into the folder Cython and CythonOpenMP (multiprocessing) provide performance of 
100 FPS for a screen 600 x 600 with water ripple effect with seabed distortion.


### Requirement 


- Pygame 3 (pip install pygame)
- Numpy    (pip install numpy)
- Cython   (refer to a tutorial to see how to install cython)
- A compiler such visual studio, MSVC, CGYWIN setup correctly
 on your system.
 - a C compiler for windows (Visual Studio, MinGW etc) install on your system 
 and linked to your windows environment.
 Note that some adjustment might be needed once a compiler is install on your system, 
 refer to external documentation or tutorial in order to setup this process.
 e.g https://devblogs.microsoft.com/python/unable-to-find-vcvarsall-bat/


### Build cython code

```script
C:\>python setup_RippleEffect.py build_ext --inplace
```
When python has been compiled, run the program main_RippleEffect.py from your favorite python IDE.

Or run the demo executable where the fodler Asset has been copied:
C:\>demo.exe


![alt text](https://github.com/yoyoberenguer/Water-Ripple-Effect/blob/master/sc3.png) 
