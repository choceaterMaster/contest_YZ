import cv2
import numpy as np
import matplotlib.pyplot as plt

def imageFFT():
    #对图像进行FFT
    img = cv2.imread('C:\\Users\\13298\\Pictures\\CSU.png',0)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    plt.subplot(121)
    plt.imshow(img, cmap = 'gray')
    plt.title('original')
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('result')
    plt.axis('off')
    plt.show()
if __name__ == '__main__':
    imageFFT()