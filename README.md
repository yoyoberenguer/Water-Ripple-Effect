# Water ripple effect and seabed distortion

Below GIF made with library PygameShader (GPU shader ==> wave_gpu method). Wave_gpu method is the cython method developped in this
github page ported to CUDA for higher resolutions and better perforamces.
For a full GPU demo install PygameShader(*) and run the demo PygameShader/Demo/GPU_demo_ripple.py 

(*) refers to the dependencies section (CUDA must be installed). 


<p align="center">
    <img src="https://github.com/yoyoberenguer/Water-Ripple-Effect/blob/master/ripples.gif?raw=true">
</p>

## Demo 
This github page host the full CPU demo, please click on the new release version 1.0.2 as shown below
<p align="left">
    <img src="https://github.com/yoyoberenguer/Water-Ripple-Effect/blob/master/Assets/Capture2.PNG?raw=true">
</p>

Click on the executable setup_RippleEffect.exe to download the installer and run it onto your machine, 
The installation process might be flagged as unsafe by your anti-virus. 

<p align="left">
    <img src="https://github.com/yoyoberenguer/Water-Ripple-Effect/blob/master/Assets/Capture1.PNG?raw=true">
</p>


## Newest version

The most recent versions of the below algorithms are now integrated within the project PygameShader, 
and will be updated from that project only.
- Water ripple effect and seabed distortion (GPU)
- Surface water ripple effect (CPU method)


## Pure Python (Compatible with Python 3.6 – 3.9)

This section describes two techniques for performing a blur effect using pure Python. These implementations are educational and prototypical in nature, and not optimized for high-performance real-time rendering.

---

### Iterative Method

**Overview**  
This approach loops through each pixel of an image (of dimensions `width × height`) and applies a blur effect by averaging the values of neighboring pixels.

**How It Works**  
- Each pixel is visited individually.
- Neighboring pixels are accessed directly using nested loops.
- The result is stored in a new image or buffer.

**Performance**  
- **Very slow**, especially for large images.
- **Not suitable** for real-time rendering above **100×100 pixels**.
- Slight speed improvements may occur in **Python 3.11+** due to interpreter optimizations.

---

### NumPy-Based Method

**Overview**  
This method uses **NumPy**'s `roll()` function to simulate directional blurring, eliminating the need for nested loops. This results in a highly vectorized and much faster computation.

**Concept**  
Each directional blur is calculated using a roll operation along a specific axis, and the resulting arrays are summed to simulate a convolution-like effect:

| Convolution Direction | Pixel Offset | NumPy Operation                     |
|------------------------|--------------|-------------------------------------|
| Down                  | (x, y + 1)   | `np.roll(array, +1, axis=0)`        |
| Up                    | (x, y - 1)   | `np.roll(array, -1, axis=0)`        |
| Left                  | (x + 1, y)   | `np.roll(array, -1, axis=1)`        |
| Right                 | (x - 1, y)   | `np.roll(array, +1, axis=1)`        |

You can sum these shifted arrays along with the original to produce a blur effect. Optionally, divide by the number of terms to average.

**Performance**  
- **Approximately 300× faster** than the pure Python loop.
- Still **not ideal** for real-time use with large resolutions.

---

   

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

