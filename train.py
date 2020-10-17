from PIL import Image
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Conv2D

number_of_image = 5
path_to_feature = "feature"


def rgb2gray(rgb):
    gray = np.mean(rgb, axis=2)
    return gray.reshape(512, 512, 1)


def get_features(labels):
    features = []
    for rgb in labels:
        gray_image = rgb2gray(rgb)
        features.append(gray_image)
    features = np.array(features)
    print("Features shape: " + str(features.shape))
    return features


def get_features_labels():
    labels = []
    for id in range(number_of_image):
        image_name = path_to_feature + "/id" + str(id) + ".jpeg"
        image = np.asarray(Image.open(image_name)) / 255
        print(image)
        labels.append(image)

    features = get_features(labels)
    labels = np.array(labels)
    print("Labels shape: " + str(labels.shape))
    return features, labels


def get_model(model_name=None):
    def create_model():
        model = Sequential()
        model.add(Conv2D(16, (3, 3), activation='relu', padding="same", input_shape=(512, 512, 1)))
        model.add(Conv2D(3, (3, 3), activation='relu', padding="same"))
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


def output_images(predictions):
    for i, prediction in enumerate(predictions):
        print(i, prediction.shape, type(prediction))
        image = (prediction * 255).astype(np.uint8)
        print(image)
        Image.fromarray(image).save('test_output/output' + str(i) + '.jpeg')


def main():
    features, labels = get_features_labels()
    cutoff = round(len(features) * .8)
    train_feature, test_feature = features[0:cutoff], features[cutoff:]
    train_label = labels[0:cutoff]
    model_name = 'test_model'
    model = get_model(model_name)
    model.fit(train_feature, train_label, epochs=20)
    model.save('keras_model/' + model_name)
    predictions = model.predict(test_feature)
    output_images(predictions)


if __name__ == '__main__':
    main()