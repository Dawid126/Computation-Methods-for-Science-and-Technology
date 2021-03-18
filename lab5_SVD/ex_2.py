import numpy as np
import imageio as im
import matplotlib.pyplot as plt


path = "tiger.jpg"
image_array = im.imread(path)
image_shape = image_array.shape[0]
num_of_iterations = [10, 100, 256, 512]
result_array = np.zeros((image_shape, image_shape, 3))
red = np.zeros((image_shape * image_shape))
green = np.zeros((image_shape * image_shape))
blue = np.zeros((image_shape * image_shape))

M1 = image_array[:, :, 0]
M2 = image_array[:, :, 1]
M3 = image_array[:, :, 2]

u1, s1, vt1 = np.linalg.svd(M1)
u2, s2, vt2 = np.linalg.svd(M2)
u3, s3, vt3 = np.linalg.svd(M3)



ut1 = u1.transpose()
ut2 = u2.transpose()
ut3 = u3.transpose()

for k in num_of_iterations:
    result = np.zeros((image_shape, image_shape))
    for i in range(k):
        matrix = s1[i] * ((ut1[i].reshape(image_shape,1)).dot(vt1[i].reshape(1,image_shape)))
        result = np.add(result, matrix)

    z = 0
    result_array[:, :, 0] = result[:, :]
    result = np.zeros((image_shape, image_shape))
    for m in range(image_shape):
        for n in range(image_shape):
            red[z] = abs(result_array[m][n][0] - image_array[m][n][0])
            z = z + 1

    for i in range(k):
        matrix = s2[i] * ((ut2[i].reshape(image_shape,1)).dot(vt2[i].reshape(1,image_shape)))
        result = np.add(result, matrix)

    z =0
    result_array[:, :, 1] = result[:, :]
    result = np.zeros((image_shape, image_shape))
    for m in range(image_shape):
        for n in range(image_shape):
            green[z] = abs(result_array[m][n][1] - image_array[m][n][1])
            z = z + 1

    for i in range(k):
        matrix = s3[i] * ((ut3[i].reshape(image_shape,1)).dot(vt3[i].reshape(1,image_shape)))
        result = np.add(result, matrix)

    z = 0
    result_array[:, :, 2] = result[:, :]
    for m in range(image_shape):
        for n in range(image_shape):
            blue[z] = abs(result_array[m][n][2] - image_array[m][n][2])
            z = z + 1

    array_to_print = np.array(result_array, dtype = np.uint8)
    im.imwrite(f'result_{k}iterations.jpg', array_to_print)
    x = range(image_shape * image_shape)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(x, red, 'ro', x, green, 'go', x, blue, 'bo',  markersize = 3)
    ax1.set(xlabel = 'Pixel', ylabel = 'Abs difference btw original and apprx' ,title = f'{k} iterations')
    fig.savefig(f'{k}iterations_difference_diagram.jpg')



