import json
import os

import pydantic
from modelplace_api import Device
from modelplace_api.utils import is_equal
from PIL import Image

from dbface import InferenceModel

dir_name = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(os.path.dirname(dir_name), "checkpoint")
test_image_path = os.path.join(dir_name, "emotion_recognition.png")
test_result_path = os.path.join(dir_name, "dbface_gt.json")

test_image = Image.open(test_image_path)
with open(test_result_path, "r") as j_file:
    test_result = json.loads(j_file.read())


def test_process_sample_dbface():
    model = InferenceModel(model_path=model_path)
    model.model_load()
    model.to_device(Device.cpu)
    ret = model.process_sample(test_image)
    ret = [pydantic.json.pydantic_encoder(item) for item in ret]
    assert is_equal(ret, test_result, error=0.03)
