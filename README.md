# WaterRippleEffect
Water ripple effect algorithm with numpy and pygame

The cython file RippleEffect.pyx contains 3 differents methods for rendering the ripple effects.
For this demo we are using a screen with dimension 300 x 300 pixels for a reasonable 77 fps 
method 1: Consist of a going through all elements from the array and perform a blur on every pixels position of the arrays (previous and current). 
As you can expect with python, this method is extremely slow and not usable for real time rendering, so forget about it. 
method 2: Using numpy array manipulation speed up the rendering by 300 times faster compare to the python loop (for r in range)
method 3: Same concept than method 2 but we are replacing numpy.roll function by our own version to gain another 1ms and reach 1.36ms
method 4: The fastest so far, 1.3 ms for each iteration 

![alt text](https://github.com/yoyoberenguer/WaterRippleEffect/blob/master/RippleEffect.gif)
![alt text](https://github.com/yoyoberenguer/WaterRippleEffect/blob/master/RippleEffect1.gif)
