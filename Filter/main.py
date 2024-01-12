import cv2
import numpy as np
from tools import *
import os, sys
import argparse



def parse_args():
    parser = argparse.ArgumentParser(description = "Image_Filter arguments")
    parser.add_argument("--mode", type = str, help = "Chose Mode : image / vod", default = "image")
    parser.add_argument("--path", type = str, help = "enter the image or vod path", default = "light_reflection.png")
    parser.add_argument("--type", type = str, help = "type : Mean / Gausian / Thresh / Optimal")
    parser.add_argument("--blursize", type = int, help = "bluersize : [5, 25]", default = 5)
    parser.add_argument("--blocksize", type = int, help = "blocksize : enter the odd number [3, 5, 7 ....]", default = 3)
    parser.add_argument("--constant", type = int, help = "constant : enter the constant", default = 0)
    parser.add_argument("--threshold", type = list, help = "threshold : [min_threshold, max_threshold]", default = [220, 255])
    # parser.add_argument("--filter", type = str, help = "filter : Blur / Binary / Erode / Sliding_Window", default = "Blur")
    if len(sys.argv) == 1:
        parser.print_help
    args = parser.parse_args()
    return args






if __name__ == "__main__":
    print("main")
    args = parse_args()
    blursize = args.blursize
    file_path = os.path.join(args.mode, args.path)
    if args.mode == "image":
        src = cv2.imread(file_path)
        cv2.imshow("origin", src)
        gray_img = preprocessing_img(src, blursize)
        
        dst = do_filter(args, gray_img)

        cv2.imshow(args.type, dst)

        se = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
        erode_img = cv2.erode(dst, se)

        cv2.imshow("erode", erode_img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    elif args.mode == "vod":
        cap = cv2.VideoCapture(file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                gray_img = preprocessing_img(frame, blursize)
                filtered_img = do_filter(args, gray_img)
                se = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
                erode_img = cv2.erode(filtered_img, se)
                
                cv2.imshow(args.type, filtered_img)
                cv2.imshow("erode", erode_img)
                
                key = cv2.waitKey(1)
                

                if key == ord("q"):
                    break
            else:
                break

    else:
        print("Unknown mode")
