# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from generate_pattern import DmdPattern
from PIL import Image, ImageDraw
import cv2
from skimage.metrics import structural_similarity as ssim
def random_image_with_shapes(width, height, num_shapes=5):
    # Create a random background
    background = np.random.randint(0, 256, (width, height, 3), dtype=np.uint8)

    # Convert the numpy array to a PIL Image
    image = Image.fromarray(background)

    # Create a drawing context to draw shapes on the image
    draw = ImageDraw.Draw(image)

    # Randomly draw shapes
    for _ in range(num_shapes):
        # Determine shape type (either rectangle or ellipse)
        shape_type = np.random.choice(["rectangle", "ellipse"])

        # Randomly determine top-left and bottom-right points for the shape
        x1, y1 = np.random.randint(0, width-30), np.random.randint(0, height-30)
        x2, y2 = x1 + np.random.randint(20, 30), y1 + np.random.randint(20, 30)

        # Randomly determine the color of the shape
        color = tuple(np.random.randint(0, 256, 3))

        if shape_type == "rectangle":
            draw.rectangle([x1, y1, x2, y2], fill=color)
        else:
            draw.ellipse([x1, y1, x2, y2], fill=color)
    grayscale_image = image.convert("L")

    # Convert the grayscale image to a 2D numpy array and return
    return np.asarray(grayscale_image)
def random_image_with_shapes(width, height, num_shapes=5):
    # Create a black background (2D array of zeros)
    background = np.zeros((width, height), dtype=np.uint8)

    # Convert the 2D numpy array to a PIL Image
    image = Image.fromarray(background, mode='L')

    # Create a drawing context to draw shapes on the image
    draw = ImageDraw.Draw(image)

    # Randomly draw shapes
    for _ in range(num_shapes):
        # Determine shape type (either rectangle or ellipse)
        shape_type = np.random.choice(["rectangle", "ellipse", "triangle"])

        # Randomly determine top-left and bottom-right points for the shape
        x1, y1 = np.random.randint(0, width-30), np.random.randint(0, height-30)
        x2, y2 = x1 + np.random.randint(20, 30), y1 + np.random.randint(20, 30)

        # Randomly determine the grayscale color of the shape (between 1 and 255 to ensure it's not black)
        color = np.random.randint(1, 256)

        if shape_type == "rectangle":
            draw.rectangle([x1, y1, x2, y2], fill=color)
        else:
            draw.ellipse([x1, y1, x2, y2], fill=color)

    # Convert the grayscale image to a 2D numpy array and return
    return np.asarray(image)


def random_pattern(width, height, sparsity):
    mask_array = [(np.random.rand(height, width) < sparsity).astype(int) for i in range(width * height)]
    return mask_array


def reconstruction_image(pattern_array, intensity_array):
    weighting_matrix = np.sum(pattern_array, axis=0)
    image_list = []
    for i in range(len(pattern_array)):
        image_list.append(intensity_array[i] * pattern_array[i])
    image_array = np.array(image_list)
    image_matrix = np.sum(image_array, axis=0) / weighting_matrix
    return image_matrix


def plot_pixel(image_matrix, title=None):
    plt.title(title)
    plt.imshow(image_matrix, cmap="gray")
    plt.show()


class SimulationCompressingImage:
    def __init__(self, input_image, light_intensity=1):
        self.light_intensity = light_intensity
        self.simulation_image = input_image
    def execute(self,pattern, reverse_pattern, sampling_rate=1, noise_rate=0):
        image = []
        image_width, image_height = self.simulation_image.shape
        num_pixel = len(pattern)
        for i in range(int(len(pattern) * sampling_rate)):
            mask = resize(pattern[i],image_width , image_height)
            reverse_mask = resize(reverse_pattern[i], image_width , image_height)
            fractional_signal = np.sum((mask * self.simulation_image)/255) / num_pixel
            reverse_fractional_signal = np.sum((reverse_mask * self.simulation_image)/255) / num_pixel

            photo_diode_signal = self.light_intensity * fractional_signal
            photo_diode_reverse_signal = self.light_intensity * reverse_fractional_signal

            # signal_noise = np.random.randint(-100,100,[self.width, self.height])/100*noise_rate*self.light_intensity
            signal_noise = np.random.randint(0, 100) / 100 * noise_rate * self.light_intensity
            reverse_signal_nose = np.random.randint(0, 100) / 100 * noise_rate * self.light_intensity
            signal = photo_diode_signal + signal_noise
            reverse_signal = photo_diode_reverse_signal + reverse_signal_nose
            image.append((signal-reverse_signal)*(mask-reverse_mask))
        image = np.sum(np.array(image), axis=0) / (int(len(pattern) * sampling_rate))
        return image
    def fourier(self,pattern, reverse_pattern, sampling_rate=1, noise_rate=0):
        image = []
        image_width, image_height = self.simulation_image.shape
        num_pixel = len(pattern)
        for i in range(int(len(pattern) * sampling_rate)):
            mask = resize(pattern[i],image_width , image_height)
            reverse_mask = resize(reverse_pattern[i], image_width , image_height)
            fractional_signal = np.sum((mask * self.simulation_image)/255) / num_pixel
            reverse_fractional_signal = np.sum((reverse_mask * self.simulation_image)/255) / num_pixel

            photo_diode_signal = self.light_intensity * fractional_signal
            photo_diode_reverse_signal = self.light_intensity * reverse_fractional_signal

            # signal_noise = np.random.randint(-100,100,[self.width, self.height])/100*noise_rate*self.light_intensity
            signal_noise = np.random.randint(0, 100) / 100 * noise_rate * self.light_intensity
            reverse_signal_nose = np.random.randint(0, 100) / 100 * noise_rate * self.light_intensity
            signal = photo_diode_signal + signal_noise
            reverse_signal = photo_diode_reverse_signal + reverse_signal_nose
            image.append((signal-reverse_signal)*(mask-reverse_mask))
        image = np.sum(np.array(image), axis=0) / (int(len(pattern) * sampling_rate))
        image = image + abs(np.min(image))
        return image
    def image_with_different_sampling_rate(self, pattern, reverse_pattern, noise_rate=0, num_image=1):
        image = []
        image_width, image_height = self.simulation_image.shape
        num_pixel = image_width**2

        summed_pattern = []
        for i in range(int(len(pattern))):
            mask = resize(pattern[i], image_width, image_height)
            reverse_mask = resize(reverse_pattern[i], image_width, image_height)
            fractional_signal = np.sum(mask * self.simulation_image)
            reverse_fractional_signal = np.sum(reverse_mask * self.simulation_image)
            photo_diode_signal =  fractional_signal
            photo_diode_reverse_signal = reverse_fractional_signal

            signal_noise = np.random.rand() * noise_rate
            reverse_signal_noise = np.random.rand() * noise_rate

            signal = photo_diode_signal + signal_noise
            reverse_signal = photo_diode_reverse_signal + reverse_signal_noise

            image.append((signal - reverse_signal) * (mask - reverse_mask))
            summed_pattern.append(mask+reverse_mask)
        image_list = []
        pattern_length = len(summed_pattern)
        steps = 1/num_image
        for i in range(1, num_image):
            print(int(pattern_length*steps))
            temp_pattern_array = np.array(summed_pattern)[0:int(pattern_length*steps)]
            image_list.append(np.sum(temp_pattern_array), axis=0)
            image_list.append(np.sum(np.array(image), axis=0))
        return image_list
    def oneside(self, pattern, sampling_rate=1, noise_rate=0):
        image = []
        image_width, image_height = self.simulation_image.shape
        num_pixel = image_width**2

        summed_pattern = []
        for i in range(int(len(pattern) * sampling_rate)):
            mask = resize(pattern[i], image_width, image_height)
            fractional_signal = np.sum(mask * self.simulation_image)/num_pixel
            photo_diode_signal =  fractional_signal

            signal_noise = np.random.rand() * noise_rate

            signal = photo_diode_signal + signal_noise

            image.append(signal * (mask))
            if np.mod(i,4)==0:
                summed_pattern.append(-1*mask)
            elif np.mod(i,4)==1:
                summed_pattern.append(1j * mask)
            elif np.mod(i,4)==2:
                summed_pattern.append(mask)
            elif np.mod(i,4)==3:
                summed_pattern.append(-1j*mask)
        summed_matrix = np.sum(np.array(summed_pattern), axis=0)

        image = np.sum(np.array(image), axis=0) / (int(len(pattern) * sampling_rate))
        #image = np.sum(np.array(image), axis=0) / summed_matrix
        #image = np.clip(image / image.max() * 255, 0, 255).astype(np.uint8)
        return image

class PSNR:
    def __init__(self, ground_image, reconstruction_image):
        self.ground_image = ground_image
        self.reconstruction_image = reconstruction_image

    def mse(self):
        """
        Compute the mean squared error between two matrices.
        """
        ground_image = self.ground_image/np.max(self.ground_image)
        reconstruction_image = self.reconstruction_image/np.max(self.reconstruction_image)

        assert ground_image.shape == reconstruction_image.shape, "Matrices must be of the same size"

        err = np.sum((ground_image - reconstruction_image) ** 2)
        err /= float(ground_image.shape[0] * reconstruction_image.shape[1])

        return err

    def execute(self):
        """
        Compute the peak signal-to-noise ratio between two matrices.
        """
        mean_square_error = self.mse()

        # Avoid division by zero
        if mean_square_error == 0:
            return float('inf')

        return 10 * np.log10(np.max(self.ground_image) ** 2 / mean_square_error)
def calculate_ssim(imageA, imageB):
    """
    Calculate the Structural Similarity Index (SSIM) between two images.
    """
    score, _ = ssim(imageA, imageB, full=True)
    return score


def mean_squared_error(imageA, imageB):
    """
    Calculate the Mean Squared Error between two images.
    Assumes both images are the same size and are numpy arrays.
    """
    # Calculate the squared difference between the images
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err
def resize(input_image, width, height):
    return cv2.resize(input_image, (width, height), interpolation=cv2.INTER_LINEAR)