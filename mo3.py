import cv2
import numpy as np

def erode(image, kernel):
    h, w = image.shape
    eroded_image = np.zeros((h, w), dtype=np.uint8)
    
    # Erozja
    for i in range(1, h-1):
        for j in range(1, w-1):
            region = image[i-1:i+2, j-1:j+2]
            eroded_image[i, j] = np.min(region * kernel)
    
    return eroded_image

def dilate(image, kernel):
    h, w = image.shape
    dilated_image = np.zeros((h, w), dtype=np.uint8)
    
    # Dylatacja
    for i in range(1, h-1):
        for j in range(1, w-1):
            region = image[i-1:i+2, j-1:j+2]
            dilated_image[i, j] = np.max(region * kernel)
    
    return dilated_image

def subtract_images(image1, image2):
    return cv2.absdiff(image1, image2)

import cv2
import numpy as np

def subtract_images(image1, image2):

    # Sprawdzenie poprawności obrazów wejściowych
    if image1 is None or image2 is None:
        raise ValueError("images cannot be None")
    if image1.shape != image2.shape:
        raise ValueError("images must have same size")
    
    # Tworzenie obrazu wynikowego o tych samych wymiarach co obrazy wejściowe
    result = np.zeros_like(image1)
    
    # Iteracja przez każdy piksel obrazów
    for i in range(image1.shape[0]):
        for j in range(image1.shape[1]):
            # Operacja odejmowania z zapewnieniem, że wartości są nieujemne
            result[i, j] = max(0, image1[i, j] - image2[i, j])
    
    return result

def process_image(image_path, output_path):
    try:
        # Wczytaj obraz binarny
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            raise ValueError("cannot load image")

        #Kernel
        kernel = np.ones((3,3), np.uint8)

        #erozja i dylatacja
        eroded = erode(image, kernel)
        dilated = dilate(image, kernel)

        # Wyznaczanie krawędzi jako różnicę między dylatacją a erozją
        edges = subtract_images(dilated, eroded)

        # Zapisanie obrazy wynikowe
        cv2.imwrite(output_path + 'original.png', image)
        cv2.imwrite(output_path + 'dilated.png', dilated)
        cv2.imwrite(output_path + 'eroded.png', eroded)
        cv2.imwrite(output_path + 'edges.png', edges)

        print("task has been successfully completed")
    except Exception as e:
        print(f"error: {e}")


process_image('binary_image.jpg', '')
