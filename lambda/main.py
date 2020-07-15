# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import sys
import os

# Setting library paths.
efs_path = "/mnt/python"
python_pkg_path = os.path.join(efs_path, "tensorflow/lib/python3.8/site-packages")
sys.path.append(python_pkg_path)

import json
import string
import time
import io
import requests

# Importing TensorFlow
import tensorflow as tf

# Loading model
model_path = os.path.join(efs_path, 'model/')
loaded_model = tf.saved_model.load(model_path)
detector = loaded_model.signatures['default']

def lambda_handler(event, context):
    r = requests.get(event['url'])
    img = tf.image.decode_jpeg(r.content, channels=3)

    # Executing inference.
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    start_time = time.time()
    result = detector(converted_img)
    end_time = time.time()

    obj = {
        'detection_boxes' : result['detection_boxes'].numpy().tolist(),
        'detection_scores': result['detection_scores'].numpy().tolist(),
        'detection_class_entities': [el.decode('UTF-8') for el in result['detection_class_entities'].numpy()] 
    }    

    return {
        'statusCode': 200,
        'body': json.dumps(obj)
    }