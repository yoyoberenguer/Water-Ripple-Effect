# Water ripple effect

### Water ripple effect
```
This Demo contains 2 different rendering methods.

#### First method 
1. Iterating method 

   Description : Iterating over all pixels values width x height and performing a blur on 
   adjacent pixels
   
   Result : Slow method and not usable for real time rendering with python with screen 
   dimension above 100 x 100 pixels!.
   This method works fine with the cython over 600 x 600 pixels

#### Second method
2. Numpy arrays


   Description : Instead of going through all the pixels values inside a loop and applying 
   a blur for each pixels, my trick is to call separately the method numpy.roll for all 
   directions (up, down, left, right) and make the sum of all 4 numpy arrays providing the
   equivalent of blur effect for each surface pixels in only 4 operations. 
   
   pixels             | numpy                            |   convolution direction 
   -------------------|----------------------------------|------------------------
   (x, y + 1)         | numpy.roll(previous, +1, axis=0) |    down pass
   (x, y - 1)         | numpy.roll(previous, -1, axis=0) |    up pass
   (x + 1, y)         | numpy.roll(previous, -1, axis=1) |    left pass
   (x - 1, y)         | numpy.roll(previous, +1, axis=1) |    right pass

   Result : Using numpy array manipulation is 300 times faster than method 1 using pure python.
      
Discover Cython version into the folder Cython and CythonOpenMP (multiprocessing).
100 FPS for a screen 600 x 600 with water ripple effect and background distortion.

#### Requirement 
- Pygame (pip install pygame)
- Numpy (pip install numpy)
- Cython (refer to a tutorial to see how to install cython and a compiler)

### Build cython code
C:\>python setup_RippleEffect.py build_ext --inplace

When python has been compiled, run the program main_RippleEffect.py from your favorite python IDE 
```


![alt text](https://github.com/yoyoberenguer/Plasma-Effect/blob/master/sc1.png) 
