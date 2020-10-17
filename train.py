from PIL import Image
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Conv2D

number_of_image = 1
path_to_feature = "/feature"


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = (r + g + b) / 3
    return gray


def get_labels(features):
    labels = []
    for rgb in features:
        gray_image = rgb2gray(rgb)
        labels.append(gray_image)
    labels = np.array(labels)
    print(labels.shape)
    return labels


def get_features_labels():
    features = []
    for id in range(number_of_image):
        image_name = path_to_feature + "id" + str(id) + ".png"
        image = np.asarray(Image.open(image_name))
        print(image.shape)
        features.append(image)

    labels = get_labels(features)
    features = np.array(features)
    print(features.shape)
    return features, labels


def get_model(model_name=None):
    def create_model():
        model = Sequential()
        model.add(Conv2D(16, (3, 3), activation='relu', inputshape=(512, 512, 3)))
        model.add(Conv2D(1, (3, 3)))
        model.compile(optimizer='adam', loss='mse')
        return model

    if model_name:
        try:
            model_l = load_model('keras_model/' + model_name)
            model_l.compile(optimizer='adam', loss='mse')
            print('Sucessfully loaded model')
            exit()
            return model_l
        except:
            print('Failed to load model. Creating new model')
            return create_model()
    else:
        print('Creating new model')
        return create_model()


def main():
    features, labels = get_features_labels()
    get_model('test_model')


if __name__ == '__main__':
    main()