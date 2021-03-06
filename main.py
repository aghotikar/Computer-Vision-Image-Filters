# Instructions:
# For question 1, only modify function: histogram_equalization
# For question 2, only modify functions: low_pass_filter, high_pass_filter, deconvolution
# For question 3, only modify function: laplacian_pyramid_blending

import os
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mtplt


def help_message():
    print("Usage: [Question_Number] [Input_Options] [Output_Options]")
    print("[Question Number]")
    print("1 Histogram equalization")
    print("2 Frequency domain filtering")
    print("3 Laplacian pyramid blending")
    print("[Input_Options]")
    print("Path to the input images")
    print("[Output_Options]")
    print("Output directory")
    print("Example usages:")
    print(sys.argv[0] + " 1 " + "[path to input image] " + "[output directory]")  # Single input, single output
    print(sys.argv[
              0] + " 2 " + "[path to input image1] " + "[path to input image2] " + "[output directory]")  # Two inputs, three outputs
    print(sys.argv[
              0] + " 3 " + "[path to input image1] " + "[path to input image2] " + "[output directory]")  # Two inputs, single output


# ===================================================
# ======== Question 1: Histogram equalization =======
# ===================================================

def histogram_equalization(img_in):
    # Write histogram equalization here

    colors=cv2.split(img_in)
    equ=[]

    # Calculate the histogram
    for color in colors:
        colorhist,cbins=np.histogram(color.flatten(), 256, [0, 256])
        cdf=colorhist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        equ.append(cdf[color])

    img_out=cv2.merge((equ[0],equ[1],equ[2]))

    cv2.imshow('final', img_out)
    cv2.waitKey(0)

    return True, img_out

def Question1():
    # Read in input images
    input_image = cv2.imread("C:/Users/Aditi/PycharmProjects/CV/input1.jpg", cv2.IMREAD_COLOR);
    succeed, output_image = histogram_equalization(input_image)

    # Write out the result
    output_name = sys.argv[3] + "1.jpg"
    cv2.imwrite(output_name, output_image)

    return True


# ===================================================
# ===== Question 2: Frequency domain filtering ======
# ===================================================

def low_pass_filter(img_in):
    # Write low pass filter here
    img_out = img_in  # Low pass filter result

    return True, img_out


def high_pass_filter(img_in):
    # Write high pass filter here
    img_out = img_in  # High pass filter result

    return True, img_out


def deconvolution(img_in):
    # Write deconvolution codes here
    img_out = img_in  # Deconvolution result

    return True, img_out


def Question2():
    # Read in input images
    input_image1 = cv2.imread(sys.argv[2], cv2.IMREAD_COLOR);
    input_image2 = cv2.imread(sys.argv[3], cv2.IMREAD_COLOR);

    # Low and high pass filter
    succeed1, output_image1 = low_pass_filter(input_image1)
    succeed2, output_image2 = high_pass_filter(input_image1)

    # Deconvolution
    succeed3, output_image3 = deconvolution(input_image2)

    # Write out the result
    output_name1 = sys.argv[4] + "2.jpg"
    output_name2 = sys.argv[4] + "3.jpg"
    output_name3 = sys.argv[4] + "4.jpg"
    cv2.imwrite(output_name1, output_image1)
    cv2.imwrite(output_name2, output_image2)
    cv2.imwrite(output_name3, output_image3)

    return True


# ===================================================
# ===== Question 3: Laplacian pyramid blending ======
# ===================================================

def laplacian_pyramid_blending(img_in1, img_in2):
    # Write laplacian pyramid blending codes here
    # generate Gaussian pyramid for A

    # Set the total number of pyramid levels
    levels = 5

    # Generate Gaussian pyramid for imgA
    gaussianPyramidA = [img_in1.copy()]
    for i in range(1, levels):
        gaussianPyramidA.append(cv2.pyrDown(gaussianPyramidA[i - 1]))

    # Generate Gaussian pyramid for imgB
    gaussianPyramidB = [img_in2.copy()]
    for i in range(1, levels):
        gaussianPyramidB.append(cv2.pyrDown(gaussianPyramidB[i - 1]))

    # Generate the inverse Laplacian Pyramid for imgA
    laplacianPyramidA = [gaussianPyramidA[-1]]
    # print 'laplacianPyramidA', len(laplacianPyramidA), len(laplacianPyramidA[0]), len(laplacianPyramidA[0][0]), len(laplacianPyramidA[0][0][0])
    # print 'gaussianPyramidA', len(gaussianPyramidA), len(gaussianPyramidA[0]), len(gaussianPyramidA[0][0]), len(laplacianPyramidA[0][0][0])
    for i in range(levels - 1, 0, -1):
        laplacian = cv2.subtract(gaussianPyramidA[i - 1], cv2.pyrUp(gaussianPyramidA[i]))
        laplacianPyramidA.append(laplacian)

    # Generate the inverse Laplacian Pyramid for imgB
    laplacianPyramidB = [gaussianPyramidB[-1]]
    for i in range(levels - 1, 0, -1):
        laplacian = cv2.subtract(gaussianPyramidB[i - 1], cv2.pyrUp(gaussianPyramidB[i]))
        laplacianPyramidB.append(laplacian)

    # Add the left and right halves of the Laplacian images in each level
    laplacianPyramidComb = []
    for laplacianA, laplacianB in zip(laplacianPyramidA, laplacianPyramidB):
        rows, cols, dpt = laplacianA.shape
        laplacianComb = np.hstack((laplacianA[:, 0:cols / 2], laplacianB[:, cols / 2:]))
        laplacianPyramidComb.append(laplacianComb)

    # Reconstruct the image from the Laplacian pyramid
    imgComb = laplacianPyramidComb[0]
    for i in range(1, levels):
        imgComb = cv2.add(cv2.pyrUp(imgComb), laplacianPyramidComb[i])

    # Display the result
    cv2.imshow('image', imgComb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    img_out = imgComb  # Blending result
    # img_out = img_in1
    return True, img_out


def Question3():
    # Read in input images
    input_image1 = cv2.imread(sys.argv[2], cv2.IMREAD_COLOR);
    # input_image1 = cv2.cvtColor(cv2.imread(sys.argv[2]), cv2.COLOR_BGR2RGB)
    input_image2 = cv2.imread(sys.argv[3], cv2.IMREAD_COLOR);
    # input_image2 = cv2.cvtColor(cv2.imread(sys.argv[3]), cv2.COLOR_BGR2RGB)

    # make images rectangular
    input_image1 = input_image1[:, :input_image1.shape[0]]
    input_image2 = input_image2[:input_image2.shape[0], :input_image2.shape[0]]
    # Laplacian pyramid blending
    succeed, output_image = laplacian_pyramid_blending(input_image1, input_image2)

    # Write out the result
    output_name = sys.argv[4] + "5.jpg"
    cv2.imwrite(output_name, output_image)

    return True


if __name__ == '__main__':
    question_number = -1

    # Validate the input arguments
    if (len(sys.argv) < 4):
        help_message()
        sys.exit()
    else:
        question_number = int(sys.argv[1])

    if (question_number == 1 and not (len(sys.argv) == 4)):
        print 'sys.argvs', sys.argv[0], sys.argv[1], sys.argv[2]
        help_message()
        sys.exit()
    if (question_number == 2 and not (len(sys.argv) == 5)):
        print 'sys.argvs', sys.argv[0], sys.argv[1], sys.argv[2]
        help_message()
        sys.exit()
    if (question_number == 3 and not (len(sys.argv) == 5)):
        print 'sys.argvs', sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
        help_message()
        sys.exit()
if (question_number > 3 or question_number < 1 or len(sys.argv) > 5):
    print("Input parameters out of bound ...")
    sys.exit()

function_launch = {
    1: Question1,
    2: Question2,
    3: Question3,
}

# Call the function
function_launch[question_number]()
