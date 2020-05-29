from keras.models import model_from_json
from main_functions import webCamera


def main():
    # load the model weights to json format
    json_file = open('model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    # load weights into new model
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model/model.h5")
    print("Loaded model from disk")

    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    # main function - open web cam & start algorithm
    webCamera(loaded_model)

if __name__ == "__main__":
    main()