import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def noise(x, y):
    """
    Generate Perlin noise at coordinates (x, y).
    """

    # Determine grid cell coordinates
    x0 = int(x) 
    x1 = x0 + 1
    y0 = int(y) 
    y1 = y0 + 1

    # Determine interpolation weights
    sx = x - x0
    sy = y - y0

    # Interpolate between grid point gradients
    n0 = dot_grid_gradient(x0, y0, x, y)
    n1 = dot_grid_gradient(x1, y0, x, y)
    ix0 = lerp(n0, n1, sx)
    n0 = dot_grid_gradient(x0, y1, x, y)
    n1 = dot_grid_gradient(x1, y1, x, y)
    ix1 = lerp(n0, n1, sx)
    # value = lerp(ix0, ix1, sy)
    value = cerp(ix0, ix1, sy)

    return value

def smooth_noise(noise_array):
    for row_index in range(20):
        for col_index in range(20):
            x_frac = row_index / float(20)
            y_frac = col_index / float(20)
            x_int = int(x_frac * 20)
            y_int = int(y_frac * 20)
            x_frac = x_int / float(20)
            x_frac = y_int / float(20)
            x_int &= 19
            y_int &= 19

            #Find weights for grid cell corners
            weight_tl = smoothstep(x_frac, y_frac)
            weight_tr = smoothstep(x_frac - 1.0, y_frac)
            weight_bl = smoothstep(x_frac, y_frac - 1.0)
            weight_br = smoothstep(x_frac - 1.0, y_frac - 1.0)
            
            #Interpolate noise values at each corner
            value = noise_array[x_int][y_int] * \
                    weight_tl + noise_array[(x_int + 1) % 20][y_int] * \
                    weight_tr + noise_array[x_int][(y_int + 1) % 20] * \
                    weight_bl + noise_array[(x_int + 1) % 20][(y_int + 1) % 20] * \
                    weight_br

            noise_array[row_index][col_index] = value

def smoothstep(x, y):
    x = 3 * x ** 2 - 2 * x ** 3
    y = 3 * y ** 2 - 2 * y ** 3
    return x * y

def dot_grid_gradient(ix, iy, x, y):
    """
    Compute the dot product between a pseudorandom gradient vector and the vector from the input coordinate to the 4D grid point.
    """
    # Compute pseudorandom gradient vector
    dx = random.uniform(-1, 1)
    dy = random.uniform(-1, 1)

    # Compute vector from input coordinate to 4D gradient point
    gradient_x = x - float(ix)
    gradient_y = y - float(iy)

    # Compute dot product
    dot_product = (dx * gradient_x + dy * gradient_y)
    return dot_product

def lerp(a, b, x):
    """
    Linearly interpolate between a and b using x.
    """
    result = a + x * (b - a)
    return result

def cerp(a, b, t):
    tangent_a = (b-a) / 2
    tangent_b = -tangent_a

    # get coefficients of cubic polynomial
    c0 = 2 * t ** 3 - 3 * t ** 2 + 1
    c1 = t ** 3 - 2 * t ** 2 + t
    c2 = -2 * t ** 3 + 3 * t ** 2
    c3 = t ** 3 - t ** 2

    # Compute the interpolated value using the cubic polynomial
    result = c0 * a + c1 * tangent_a + c2 * b + c3 * tangent_b

    return result

def generate_perlin_noise(width, height, octaves=2, persistence=0.5, lacunarity=2.0):
    """
    Generate a 2D array of Perlin noise with the specified dimensions and octaves.
    """
    noise_array = [[0.0] * height for i in range(width)]
    max_amplitude = sum([persistence ** i for i in range(octaves)])
    amplitude = 0.8
    frequency = 0.3

    # Generate octaves
    for o in range(octaves):
        for x in range(width):
            for y in range(height):
                noise_array[x][y] += noise(x * frequency, y * frequency) * amplitude

        # Update amplitude and frequency for next octave
        amplitude *= persistence
        frequency *= lacunarity
        max_amplitude += amplitude


    # Normalize the noise array
    for x in range(width):
        for y in range(height):
            noise_array[x][y] /= max_amplitude
   
    # smooth_noise(noise_array)

    print(f"Before gaussian_filter:\n{noise_array}\n\n")
    noise_array = gaussian_filter(noise_array, 1.7)
    
    #minMaxNormalize
    maxValue = np.amax(np.array(noise_array))
    minValue = np.amin(np.array(noise_array))
    for x in range(width):
        for y in range(height):
            noise_array[x][y] = -1 * (noise_array[x][y] - minValue) / (minValue - maxValue)
    print(f"After gaussian_filter and minmax norm:\n{noise_array}\n\n")
    
    plt.hist(np.array(noise_array).flatten(), bins=10)
    plt.show()
    return noise_array

if __name__ == '__main__':
    random.seed('brad')
    perlin_map = generate_perlin_noise(20, 20, 5, 0.2, 5)
    print(perlin_map)
    perlin_map = np.array(perlin_map)

    plt.imshow(perlin_map, cmap='gray')
    plt.show()
