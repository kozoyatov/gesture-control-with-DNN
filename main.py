import serial
ser1 = serial.Serial('COM5', 9600)
import keras
from keras_preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input
from keras.models import model_from_json
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import enum


class Type(enum.Enum):
  train = 1
  test = 2

class Image:
  def __init__(self, path,folderName):
    self.path = path
    self.folderName = folderName
    self.data=[]
    self.type = Type

def setData(self):
    self.data=self.folderName.find('1')

def prepar_image(img):
    x=cv2.resize(img,(224,224))
    x=image.img_to_array(x)
    x=np.expand_dims(x,axis=0)
    x=preprocess_input(x)
    return x

def webCamera(model):
    cap = cv2.VideoCapture(0)
    first_time = True
    i = 0
    frame_pix = 3
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255, 0, 0)
    lineType = 2
    counter_1 = 0
    counter_2 = 0

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        i+=1

        fliped = cv2.flip(frame, 1)
        if i>3:
            if first_time:
                first_frame = fliped
                cropped_first = first_frame[50 + frame_pix:250 - frame_pix, 384 + frame_pix:584 - frame_pix].copy()
                cv2.imshow('frame', cropped_first)
                first_time = False

            draw_img = cv2.rectangle(fliped,(384,50),(584,250),(0,255,0),frame_pix)
            cropped = draw_img[50+frame_pix:250-frame_pix,384+frame_pix:584-frame_pix].copy()
            prediction = model.predict(prepar_image(cropped))

            if (prediction[0][1] > 0.75):
                counter_1 = 0
                counter_2 += 1
                send = 'p'
                if counter_2 > 10:
                    draw_img[50 + frame_pix:250 - frame_pix, 384 + frame_pix:584 - frame_pix] = cv2.putText(draw_img[50 + frame_pix:250 - frame_pix, 384 + frame_pix:584 - frame_pix], '2', (0, 40), font,fontScale, fontColor, lineType)
                    counter_2 = 0
                    ser1.write(send.encode())
                    print('2')
                    draw_img = cv2.rectangle(fliped, (384, 50), (584, 250), (0, 0, 255), frame_pix)
                    cv2.imshow('frame', draw_img)
                    cv2.waitKey(800)

                else:
                    draw_img = cv2.rectangle(fliped, (384, 50), (584, 250), (0, 0, 255), frame_pix)
                    cv2.imshow('frame', draw_img)

            elif (prediction[0][2] > 0.75):
                counter_1 += 1
                counter_2 = 0
                send = 'n'
                if counter_1 > 10:
                    draw_img[50 + frame_pix:250 - frame_pix, 384 + frame_pix:584 - frame_pix] = cv2.putText(draw_img[50 + frame_pix:250 - frame_pix, 384 + frame_pix:584 - frame_pix], '1', (0, 40), font,fontScale, fontColor, lineType)
                    counter_1 = 0
                    ser1.write(send.encode())
                    print('1')
                    draw_img = cv2.rectangle(fliped, (384, 50), (584, 250), (0, 0, 255), frame_pix)
                    cv2.imshow('frame', draw_img)
                    cv2.waitKey(800)

                else:
                    draw_img = cv2.rectangle(fliped, (384, 50), (584, 250), (0, 0, 255), frame_pix)
                    cv2.imshow('frame', draw_img)

            elif (prediction[0][0] > 0.75):
                cv2.imshow('frame', draw_img)

            else:
                cv2.imshow('frame', draw_img)


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def main():
    json_file = open('model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model/model.h5")
    print("Loaded model from disk")
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    webCamera(loaded_model)

if __name__ == "__main__":
    main()