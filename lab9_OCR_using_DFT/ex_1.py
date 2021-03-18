import numpy as np
import copy
from PIL import Image
from PIL import ImageOps
import matplotlib.pyplot as plt
import matplotlib.patches as ptch


def save_image_as_chart(array_image, file_name, title ="", x_label = "", y_label = ""):
    height, width = np.shape(array_image)
    fig, ax1 = plt.subplots(figsize=(width/50, height/50))
    ax1.imshow(array_image, cmap= "gray")
    ax1.set(xlabel=x_label, ylabel=y_label, title=title)
    fig.savefig(file_name + ".png")

def save_image_as_chart_with_markes(array_image, markers_location, marker_shapes,
                                    file_name, title ="", x_label = "", y_label = ""):

    height, width = np.shape(array_image)
    fig, ax1 = plt.subplots(figsize=(width / 50, height / 50))
    ax1.imshow(array_image, cmap="gray")
    ax1.set(xlabel=x_label, ylabel=y_label, title=title)

    for i in range(np.shape(markers_location)[0]):
        for j in range(np.shape(markers_location)[1]):
            if markers_location[i, j] != 0:
                mark = ptch.Rectangle((j, i), - marker_shapes[1], - marker_shapes[0], linewidth=1,
                                      edgecolor="r", facecolor="none")
                ax1.add_patch(mark)

    #fig.savefig(file_name + ".png")
    plt.show()


def plot_modules_and_phases(image_path):
    image = Image.open(image_path).convert('L')
    array_image = np.asarray(image)
    freq_array = np.fft.fftshift(np.fft.fft2(array_image))

    mods = np.absolute(freq_array)
    mods = np.log(mods)

    save_image_as_chart(mods, "modules", "Fourier coeffs modules")
    phases = np.angle(freq_array)
    save_image_as_chart(phases, "phases", "Fourier coeffs phases")


def compute_correlation(loaded_image, loaded_pattern, coeff):
    image_array = np.asarray(loaded_image)
    pattern_array = np.asarray(loaded_pattern)
    pattern_array_rotated = np.rot90(pattern_array, 2)

    pattern_fft = np.fft.fft2(pattern_array_rotated, np.shape(image_array))
    image_fft = np.fft.fft2(image_array)

    correlation_array = np.real(np.fft.ifft2(np.multiply(pattern_fft, image_fft)))
    max = np.max(correlation_array)
    for i in range(np.shape(correlation_array)[0]):
        for j in range(np.shape(correlation_array)[1]):
            if(correlation_array[i,j] < max * coeff):
                correlation_array[i,j] = 0

    return correlation_array


def find_pattern(image_path, pattern_path, coeff, invert=True):
    image = Image.open(image_path).convert('L')
    pattern = Image.open(pattern_path).convert('L')
    image_original = copy.deepcopy(image)
    if(invert):
        pattern = ImageOps.invert(pattern)
        image = ImageOps.invert(image)

    correlation_array = compute_correlation(image, pattern, coeff)
    num_of_patterns_found = np.count_nonzero(correlation_array)

    file_name = "marked_patterns_image_" + pattern_path.split("/")[0] + "_" + pattern_path.split("/")[1].split(".")[0]
    save_image_as_chart_with_markes(image_original, correlation_array, np.shape(pattern),
                        file_name, f"Number of patterns found :{num_of_patterns_found}")


plot_modules_and_phases("roboto-slab/roboto-slab-text.png")
find_pattern("roboto-slab/roboto-slab-text.png", "roboto-slab/dot.png", 0.9)
find_pattern("roboto-slab/roboto-slab-text.png", "roboto-slab/k.png", 0.9)
find_pattern("fish_images/school.jpg", "fish_images/fish1.png", 0.7, invert = False)

