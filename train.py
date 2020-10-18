from PIL import Image
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Conv2D

number_of_image = 299


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
        image_name = "feature/id" + str(id) + ".jpeg"
        image = np.asarray(Image.open(image_name)) / 255
        labels.append(image)

    features = get_features(labels)
    labels = np.array(labels)
    print("Labels shape: " + str(labels.shape))
    return features, labels


def get_model(model_name=None):
    def create_model():
        model = Sequential()
        model.add(Conv2D(16, (3, 3), activation='relu', padding="same", input_shape=(512, 512, 1)))
        model.add(Dropout(.2))
        model.add(Conv2D(16, (3, 3), activation='relu', padding="same"))
        model.add(Dropout(.2))
        model.add(Conv2D(3, (3, 3), activation='relu', padding="same"))
        model.compile(optimizer='adam', loss='mse')
        return model

    if model_name:
        try:
            model_l = load_model('keras_model/' + model_name)
            model_l.compile(optimizer='adam', loss='mse')
            print('Sucessfully loaded model')
            return model_l, True
        except:
            print('Failed to load model. Creating new model')
            return create_model(), False
    else:
        print('Creating new model')
        return create_model(), False


def output_images(predictions, to, start_index):
    for i, prediction in enumerate(predictions):
        image = (prediction * 255).astype(np.uint8)
        Image.fromarray(image).save(to + str(i + start_index) + '.jpeg')


def input_images(arr, to, start_index):
    for i, prediction in enumerate(arr):
        image2 = np.zeros((512, 512, 3))
        image2[:, :, 0] = prediction.reshape(512, 512)
        image2[:, :, 1] = prediction.reshape(512, 512)
        image2[:, :, 2] = prediction.reshape(512, 512)
        image = (image2 * 255).astype(np.uint8)
        Image.fromarray(image).save(to + str(i + start_index) + '.jpeg')


def main():
    features, labels = get_features_labels()
    cutoff = round(len(features) * .8)
    train_feature, test_feature = features[0:cutoff], features[cutoff:]
    train_label, test_label = labels[0:cutoff], labels[cutoff:]
    model_name = 'best_model'
    model, loaded = get_model(model_name)
    if not loaded:
        for i in range(1000):
            model.fit(train_feature, train_label, validation_data=(test_feature, test_label), epochs=1)
            model.save('keras_model/' + model_name + str(i))
    predictions = model.predict(test_feature)
    input_images(test_feature, 'test_input/input', cutoff)
    output_images(predictions, 'test_output/output', cutoff)


if __name__ == '__main__':
    main()