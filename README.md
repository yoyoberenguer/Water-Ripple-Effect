# Water ripple effect

### Water ripple effect algorithm with numpy and pygame

The pyx file RippleEffect contains 3 different methods for rendering the ripple effects.
For this demo we are using a screen with dimension 300 x 300 pixels to get a reasonable 77 fps 

1. Iterating method

   Iterating over an array and performing a blur on adjacent pixels like :

    pixel left | pixel right | pixel up   | down | 
   ------------|-------------|------------|------|
   (x + 1, y)  | (x - 1, y)  | (x, y - 1) | (x, y + 1)

   As you can expect with python, this method is extremely slow and not usable for real time rendering with screen 
   dimension over 100 x 100 pixels!.

2. Numpy 

   Instead of going through all the values (300 x 300) within a loop, we can simplify the amount of calculation with only
   4 numpy array manipulation instead.

   For pixels (x, y + 1), we can shift vertically all the values at once instead of going through them one by one such as      
   numpy.roll(previous, 1, axis=0).

   ```
   e.g

   array([

          [ 0.,  0.,  0.,  0.],      
          [ 0.,  0.,  0.,  0.],     
          [ 0.,  0.,  0.,  0.],     
          [ 0.,  0.,  0.,  0.]])

   a[0, 0] = 255

   array([

          [ 255.,    0.,    0.,    0.],
          [   0.,    0.,    0.,    0.],
          [   0.,    0.,    0.,    0.],
          [   0.,    0.,    0.,    0.]])

   numpy.roll(a, 1, axis=0).

   array([

          [   0.,    0.,    0.,    0.],
          [ 255.,    0.,    0.,    0.],
          [   0.,    0.,    0.,    0.],
          [   0.,    0.,    0.,    0.]])
   ```

   as you can see the values are shifted to the bottom of the screen. 


   pixels             | numpy 
   -------------------|-----------------------------------
   (x, y + 1)         | numpy.roll(previous, +1, axis=0)
   (x, y - 1)         | numpy.roll(previous, -1, axis=0)
   (x + 1, y)         | numpy.roll(previous, -1, axis=1)
   (x - 1, y)         | numpy.roll(previous, +1, axis=1)

   Using numpy array manipulation is 300 times faster than method 1

3. Same concept than method 2 but we are replacing numpy.roll by our own version to increase the speed around 1.36ms

4. Is the fastest so far with 1.3 ms/iter.

_A multiprocessing method will be implemented soon for rendering the ripple effect with surface distortion on 
full screen with hopefully 60 fps._ 

![alt text](https://github.com/yoyoberenguer/WaterRippleEffect/blob/master/RippleEffect.gif)
![alt text](https://github.com/yoyoberenguer/WaterRippleEffect/blob/master/RippleEffect1.gif)
