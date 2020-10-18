from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

path_to_model = "keras_model/best_model"
path_to_image = "sample.jpeg"


def main():
    gray_scale_image = np.array([np.asarray(Image.open(path_to_image))[:, :, 0].reshape(512, 512, 1) / 255])
    model = load_model(path_to_model)
    prediction = model.predict(gray_scale_image)
    image = (prediction * 255).astype(np.uint8)[0]
    Image.fromarray(image).save('colored_image.jpeg')


if __name__ == '__main__':
    main()