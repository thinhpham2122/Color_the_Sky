from PIL import Image
import numpy as np

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


def main():
    features, labels = get_features_labels()


if __name__ == '__main__':
    main()