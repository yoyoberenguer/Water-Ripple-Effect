# WaterRippleEffect
Water ripple effect algorithm with numpy and pygame

The cython file RippleEffect.pyx contains 3 differents methods for rendering the ripple effects.
For this demo we are using a screen with dimension 300 x 300 pixels for a reasonable 77 fps 

method 1: Consist of a going through all elements from the array and performing a blur on every adjacent pixels (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1) of the array (previous). As you can expect with python, this method is extremely slow and not usable for real time rendering of screen over the dimensions 100 x 100 pixels.

# method 2
# Instead of going through all the values 300 x 300 with a loop, we can simplify the amount of calculation with
# 4 numpy manipulation,
# for pixels (x, y + 1) we can shift vertically all the values at once instead of going through them one
# by one using the power of numpy array --> numpy.roll(previous, 1, axis=0).
# e.g
# array([[ 0.,  0.,  0.,  0.],
#        [ 0.,  0.,  0.,  0.],
#        [ 0.,  0.,  0.,  0.],
#        [ 0.,  0.,  0.,  0.]])
# >>> a[0, 0] = 255
# >>> a
# array([[ 255.,    0.,    0.,    0.],
#        [   0.,    0.,    0.,    0.],
#        [   0.,    0.,    0.,    0.],
#        [   0.,    0.,    0.,    0.]])
# gives
# array([[   0.,    0.,    0.,    0.],
#        [ 255.,    0.,    0.,    0.],
#        [   0.,    0.,    0.,    0.],
#        [   0.,    0.,    0.,    0.]])
# as you can see the value is shifted to the bottom of the screen
# The same way we can process the pixels (x, y - 1) with numpy.roll(previous, -1, axis=0)
# and son on:
# pixels (x + 1, y) --> numpy.roll(previous, -1, axis=1)
# pixels (x - 1, y) --> numpy.roll(previous, +1, axis=1)
# This method improved considerably the rendering time e.g
# method 1
# print(timeit.timeit('ripple_1(cols, rows, previous, current)',
#                        'from __main__ import ripple_1, cols, rows, previous, current', number=10))
# gives 8.11 seconds with a screen size of 300 x 300 pixels for only 10 iterations (0.811 secs for one iter)
# print(timeit.timeit('ripple_2(previous, current)',
#                         'from __main__ import ripple_2, previous, current', number=1000))
# gives 2.69 seconds with a screen of 300 x 300 pixels, 1000 iterations (2.6ms for 1 iter)

method 2: Using numpy array manipulation is 300 times faster compare to method 1

method 3: Same concept than method 2 but we are replacing numpy.roll function by our own version to gain another 1ms and reach 1.36ms

method 4: The fastest so far, 1.3 ms for each iteration 

![alt text](https://github.com/yoyoberenguer/WaterRippleEffect/blob/master/RippleEffect.gif)
![alt text](https://github.com/yoyoberenguer/WaterRippleEffect/blob/master/RippleEffect1.gif)
