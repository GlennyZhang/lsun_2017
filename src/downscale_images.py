"""
No time, no resources => Let's downscale images
"""
from __future__ import division

import os
from joblib import Parallel, delayed
import cv2

min_size = 192


def downscale(old_file_name):
    img = cv2.imread(os.path.join(old_file_name))

    new_file_name = (old_file_name
                     .replace('training', 'training_' + str(min_size))
                     .replace('validation', 'validation_' + str(min_size))
                     .replace('testing', 'testing_' + str(min_size))
                     )

    height, width, _ = img.shape

    if width > height:
        new_width = int(1.0 * width / height * min_size)
        new_height = min_size

    else:
        new_height = int(1.0 * height / width * min_size)
        new_width = min_size

    img_new = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(new_file_name, img_new)

if __name__ == '__main__':
    data_path = '../data'

    for image_set in ['training', 'validation', 'testing']:
        try:
            print os.path.join(data_path, image_set + '_' + str(min_size))
            os.mkdir(os.path.join(data_path, image_set + '_' + str(min_size)))
        except:
            pass

        for subset in ['images', 'instances', 'labels']:
            try:
                os.mkdir(os.path.join(data_path, image_set + '_' + str(min_size), subset))
            except:
                pass

    # for image_set in ['training', 'validation']:
    #     for subset in ['images', 'instances', 'labels']:
    #         target_path = os.path.join(data_path, image_set, subset)
    #         file_names = os.listdir(target_path)
    #         file_names = [os.path.join(target_path, file_name) for file_name in file_names]
    #
    #         result = Parallel(n_jobs=8)(delayed(downscale)(r) for r in file_names)

    for image_set in ['testing']:
        for subset in ['images']:
            target_path = os.path.join(data_path, image_set, subset)
            file_names = os.listdir(target_path)
            file_names = [os.path.join(target_path, file_name) for file_name in file_names]

            result = Parallel(n_jobs=8)(delayed(downscale)(r) for r in file_names)
