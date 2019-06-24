# Water ripple effect

### Water ripple effect with fast python algorithm using numpy and pygame.

This Demo contains 2 different rendering methods.
The pygame display is set to 300 x 300 pixels for the presentation but those values can be adjusted at your convenience, bare
in mind that the animation speed will ne impacted by the screen dimensions.

#### First method 
1. Iterating method 

   Description : Iterating over all pixels values width x height and performing a blur on adjacent pixels
   
   Result : Slow method and not usable for real time rendering with python with screen dimension above 100 x 100 pixels!.
   However this method works fine with C or Java.
   
#### Second method
2. Numpy arrays

   Description : Instead of going through all the pixels values inside a loop and applying a blur for each pixels, 
   my trick is to call separately the method numpy.roll for all directions (up, down, left, right) and make the sum of all 4 numpy            arrays providing a blur effect in only 4 operations using convolution properties.  
   
   pixels             | numpy                            |   convolution direction 
   -------------------|----------------------------------|------------------------
   (x, y + 1)         | numpy.roll(previous, +1, axis=0) |    down pass
   (x, y - 1)         | numpy.roll(previous, -1, axis=0) |    up pass
   (x + 1, y)         | numpy.roll(previous, -1, axis=1) |    left pass
   (x - 1, y)         | numpy.roll(previous, +1, axis=1) |    right pass

   Result : Using numpy array manipulation is 300 times faster than method 1

_A multiprocessing method will be implemented soon for rendering the ripple effect with surface distortion on 
full screen with hopefully 60 fps._ 

![alt text](https://github.com/yoyoberenguer/WaterRippleEffect/blob/master/RippleEffect.gif)
![alt text](https://github.com/yoyoberenguer/WaterRippleEffect/blob/master/RippleEffect1.gif)
