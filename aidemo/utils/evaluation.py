from os import path
from PIL import Image
import numpy as np
import io
from django.core.files.images import ImageFile
import matplotlib.pyplot as plt
# %matplotlib inline
from .segment_model import SegmentationModel
from image.models import SegmentModel

import numpy as np
import cv2

def overlay_mask(image, mask, alpha=0.5, rgb=[255, 0, 0]):
	
	overlay = image.copy()
	overlay[mask] = np.array(rgb, dtype=np.uint8)

	output = image.copy()
	cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

	return output

def plot_results(test_data, image, score, figsize=(3,3)):
    
    building_score = score[1]
    
    building_mask_pred = (np.argmax(score, axis=0) == 1)
    building_overlay_pred = overlay_mask(image, building_mask_pred)
    
    # building_mask_gt = (label > 0)
    # building_overlay_gt = overlay_mask(image, building_mask_gt)
    
    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(3*figsize[0], figsize[1]))
    
    ax0.imshow(image)
    ax0.set_title('Input') 
    
    ax1.imshow(building_score, vmin=0.0, vmax=1.0)
    ax1.set_title('Predicted Building Score') 
    

    print(type(building_score))
    # 640 x 480
    # array = np.reshape(building_overlay_pred, (640, 480))

    data = Image.fromarray(building_score)
    mem_imge = io.BytesIO()
    data.save(mem_imge, 'tiff')

    output = ImageFile(mem_imge)

    ax2.imshow(building_overlay_pred)
    ax2.set_title('Input + Predicted Buildings') 
    
    figure = io.BytesIO()
    # plt.plot(xvalues, yvalues)
    plt.savefig(figure, format="png")
    content_file = ImageFile(figure)
    return content_file, output
    # # ax3.imshow(building_overlay_gt)
    # # ax3.set_title('Input + Ground Truth Buildings') 
    # plt.savefig('foo.png')
    # plt.show()


def evaluate(image_path, type):
    mean = np.load(path.join(path.dirname(__file__), 'mean.npy'))

    if type == SegmentModel.TYPE_UNET:
        model = SegmentationModel(path.join(path.dirname(__file__), 'model_iter_3035'), mean)
    elif type == SegmentModel.TYPE_RESNET:
        model = SegmentationModel(path.join(path.dirname(__file__), 'model_iter_2428'), mean)

    # image_path = path.join(path.dirname(__file__),'3band_AOI_1_RIO_img6931.tif')

    image = np.array(Image.open(image_path))
    # label = np.array(Image.open(label_path))
    score = model.apply_segmentation(image)
    
    image = plot_results(image_path, image, score)
    return image
