#TESTING done in this file using the trained model... Code for saving the detected images to csv and also calcuates the areas
#It will generate a new dataset that has filename,label dimensions of the detected lakes and also their areas
#The input of this file are the imges in which detection was done
#The model path is the path to the trained folder

import numpy as np
import argparse
import os
import tensorflow as tf
from PIL import Image
from io import BytesIO
import glob
import matplotlib.pyplot as plt

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import csv

utils_ops.tf = tf.compat.v1


tf.gfile = tf.io.gfile


def load_model(model_path):
    model = tf.saved_model.load(model_path)
    return model


def load_image_into_numpy_array(path):
   
    img_data = tf.io.gfile.GFile(path, 'rb').read()
    image = Image.open(BytesIO(img_data))
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)




def run_inference_for_single_image(model, image):
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run inference
    output_dict = model(input_tensor)

  
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key: value[0, :num_detections].numpy()
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            output_dict['detection_masks'], output_dict['detection_boxes'],
            image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

    return output_dict

def save_results_to_csv(csv_path, image_filename, output_dict, category_index, min_score_thresh=0.1):
    
    with open(csv_path, mode='a', newline='') as csv_file:
        fieldnames = ['Filename', 'Label', 'XMin', 'YMin', 'XMax', 'YMax', 'Area']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        

        for i in range(output_dict['num_detections']):
            score = output_dict['detection_scores'][i]
            if score >= min_score_thresh:
                label_id = output_dict['detection_classes'][i]
                label = category_index[label_id]['name']

                bbox = output_dict['detection_boxes'][i]
                x_min, y_min, x_max, y_max = bbox[1], bbox[0], bbox[3], bbox[2]
                area = (x_max - x_min) * (y_max - y_min)

                writer.writerow({
                    'Filename': image_filename,
                    'Label': label,
                    'XMin': x_min,
                    'YMin': y_min,
                    'XMax': x_max,
                    'YMax': y_max,
                    'Area': area
                })



def run_inference(model, category_index, image_path):
    if os.path.isdir(image_path):
        image_paths = []
        for file_extension in ('*.png', '*jpg'):
            image_paths.extend(glob.glob(os.path.join(image_path, file_extension)))
        
        for i_path in image_paths:
            image_np = load_image_into_numpy_array(i_path)
            # Actual detection.
            output_dict = run_inference_for_single_image(model, image_np)
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                output_dict['detection_boxes'],
                output_dict['detection_classes'],
                output_dict['detection_scores'],
                category_index,
                instance_masks=output_dict.get('detection_masks_reframed', None),
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=0.1)
            csv_path = "2016Areas.csv"
            
            save_results_to_csv(csv_path, os.path.basename(i_path), output_dict, category_index)
            plt.imshow(image_np)
            # plt.show() print(output_dict)

            #Code that enables the output images to have the same name as the input image to diffrenciate
            image_base_name = os.path.splitext(os.path.basename(i_path))[0]
            output_file_path = "outputs/2016Images/detected{}.png".format(image_base_name)
            plt.savefig(output_file_path)

            
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect objects inside webcam videostream')
    parser.add_argument('-m', '--model', type=str, required=True, help='Model Path')
    parser.add_argument('-l', '--labelmap', type=str, required=True, help='Path to Labelmap')
    parser.add_argument('-i', '--image_path', type=str, required=True, help='Path to image (or folder)')
    args = parser.parse_args()

    detection_model = load_model(args.model)
    category_index = label_map_util.create_category_index_from_labelmap(args.labelmap, use_display_name=True)
    


    run_inference(detection_model, category_index, args.image_path)

