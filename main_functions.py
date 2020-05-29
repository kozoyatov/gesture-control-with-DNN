import keras
from keras_preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input
import cv2
import numpy as np
import serial

# Arduino usb connection
ser1 = serial.Serial('COM5', 9600)

x_width = 384
y_width = 50
rec_width = 200
frame_pix = 3
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (0, 0, 255)
lineType = 2

def prepar_image(img):
    # prepar image before DNN model
    x = cv2.resize(img, (224, 224))
    x = image.img_to_array(x)
    x = np.expand_dims(x,axis=0)
    x = preprocess_input(x)
    return x

def draw_image(draw_img,ges_num):
    draw_img[y_width + frame_pix:y_width + rec_width - frame_pix, x_width + frame_pix:x_width + rec_width - frame_pix] = cv2.putText(draw_img[y_width + frame_pix:y_width + rec_width - frame_pix,x_width + frame_pix:x_width + rec_width - frame_pix], ges_num, (0, 40), font, fontScale, fontColor, lineType)

def webCamera(model):
    cap = cv2.VideoCapture(0)
    i = 0
    counter_1 = 0
    counter_2 = 0
    pred_threshold = 0.75
    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()
        i += 1
        flipped = cv2.flip(frame, 1)

        if i > 3:  # pass initial frames

            draw_img = cv2.rectangle(flipped, (x_width,y_width), (x_width + rec_width,y_width + rec_width), (0, 255, 0), frame_pix)  # draw green rectangle
            cropped = draw_img[y_width+frame_pix:y_width + rec_width-frame_pix, x_width+frame_pix:x_width + rec_width - frame_pix].copy()
            prediction = model.predict(prepar_image(cropped))  # model prediction - list of 3 probabilities

            if prediction[0][1] > pred_threshold: # model predict gesture 2
                counter_1 = 0
                counter_2 += 1
                send = 'p'
                if counter_2 > 10:  # counting 10 frames with same prediction
                    draw_image(draw_img, '2')
                    counter_2 = 0
                    ser1.write(send.encode())
                    print('2')
                    draw_img = cv2.rectangle(flipped, (x_width, y_width), (x_width + rec_width, y_width + rec_width), (0, 0, 255), frame_pix)
                    cv2.imshow('frame', draw_img)
                    cv2.waitKey(1000)

                else:
                    draw_img = cv2.rectangle(flipped, (x_width, y_width), (x_width + rec_width, y_width + rec_width), (0, 0, 255), frame_pix)
                    cv2.imshow('frame', draw_img)

            elif prediction[0][2] > pred_threshold:  # model predict gesture 2
                counter_1 += 1
                counter_2 = 0
                send = 'n'

                if counter_1 > 10:   # counting 10 frames with same prediction
                    draw_image(draw_img, '1')
                    counter_1 = 0
                    ser1.write(send.encode())
                    print('1')
                    cv2.imshow('frame', draw_img)
                    cv2.waitKey(1000)

                else:
                    draw_img = cv2.rectangle(flipped, (x_width, y_width), (x_width + rec_width, y_width + rec_width), (0, 0, 255), frame_pix)
                    cv2.imshow('frame', draw_img)

            else:
                cv2.imshow('frame', draw_img)
            cv2.waitKey(1)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
