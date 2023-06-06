import os.path as osp 


import cv2 
import numpy as np 
from PIL import Image
from absl import app, logging  # argparse 대용인가?; (ref) https://github.com/abseil/abseil-py
import tensorflow as tf 
from tensorflow.python.saved_model import tag_constants
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

import core.utils as utils
from core.yolov4 import filter_boxes

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
else:
    print("No GPU")


def model_inference(image_list):

    interpreter = tf.lite.Interpreter(model_path="./checkpoints/yolov4-tiny-416.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

#    print(input_details)
#    print(output_details)

    interpreter.set_tensor(input_details[0]['index'], image_list)
    interpreter.invoke()
    pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]

    boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25, input_shape=tf.constant([416, 416]))

    return  boxes, pred_conf 



def run_object_detection(image):

    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    input_size = 416

    image_data = cv2.resize(image, (input_size, input_size))
    image_data = image_data / 255.

    image_list = []

    for i in range(1):
        image_list.append(image_data)
    image_list = np.asarray(image_list).astype(np.float32) 

    boxes, pred_conf = model_inference(image_list)

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape( pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=0.45,
        score_threshold=0.75
        )    


    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
    image, coordinates, barycenter = utils.draw_bbox(image, pred_bbox)

    image = Image.fromarray(image.astype(np.uint8))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    return image, coordinates, barycenter

