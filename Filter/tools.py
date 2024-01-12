import cv2
import numpy as np


def preprocessing_img(src, blursize):
    width_ = 400
    height_ = 300
    resized_img = cv2.resize(src, (width_, height_))
    
    # top_gap_proportion = 0.4
    # bot_gap_proportion = 0.1
    # top_height_proportion = 0.5
    # bot_height_proportion = 0.9

    # width_offset = 25

    # extra_up = 0
    # extra_down = 0

    # top_gap = width_ * top_gap_proportion
    # bot_gap = width_ * bot_gap_proportion
    # top_height = height_ * top_height_proportion
    # bot_height = height_ * bot_height_proportion

    # corners_ = np.float32([[top_gap + width_offset, top_height],
    #                     [(width_ - top_gap) + width_offset + 15, top_height],
    #                     [bot_gap + width_offset, bot_height],
    #                     [(width_ - bot_gap) + width_offset, bot_height]])

    # warpCorners_ = np.float32([[extra_up, 0.0],
    #                         [width_ - extra_up, 0.0],
    #                         [extra_down, height_],
    #                         [width_ - extra_down, height_]])
    # trans_matrix = cv2.getPerspectiveTransform(corners_, warpCorners_)
    # warped_img = cv2.warpPerspective(resized_img, trans_matrix, (width_, height_))

    blur_img = cv2.GaussianBlur(resized_img, (blursize, blursize), 0, 0, cv2.BORDER_DEFAULT)
    gray_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)


    return gray_img


def do_filter(args, gray_img):
    dst = None
    
    if args.type == "Mean":
        dst = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                    blockSize = args.blocksize, C = args.constant)
    elif args.type == "Gausian":
        dst = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                    blockSize = args.blocksize, C = args.constant)
    elif args.type == "Thresh":
        ret, dst = cv2.threshold(gray_img, args.threshold[0], args.threshold[1], cv2.THRESH_BINARY)

    elif args.type == "Optimal":
        ret, dst = cv2.threshold(gray_img, args.threshold[0], args.threshold[1], cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    else:
        print("Unknown type")

    return dst
