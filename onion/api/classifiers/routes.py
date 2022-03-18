import base64
import io

from PIL import Image
from flask import Blueprint, current_app
from flask_restx import reqparse, Resource

import json

from onion.api.classifiers.models import pretrained_classifiers

classifiers_blueprint = Blueprint('classifiers', __name__)


@classifiers_blueprint.route('/classifiers', methods=['GET', 'POST'])
def get_classifiers():
    """Get a list of all classifiers.
    """
    return json.dumps({
        "flag": True,
        "data": [{
            "name": classifier.name,
            "paper": classifier.paper
        } for classifier in pretrained_classifiers]
    })


parser = reqparse.RequestParser()
parser.add_argument('image_name', required=True)
parser.add_argument('classifier')


@classifiers_blueprint.route('/classify', methods=['GET', 'POST', 'put'])
def classify():
    """Classify image with pre-trained classifier.

        Parameters
        ----------
        -  image_data:
        Base64-encoded image.
        -  classifier_id:
        Classifier identifier. Integer.


        Returns
        -------
        List of JSON, where each JSON has the form:
        {
            "index": class index,
            "label": label (name of class index),
            "percentage": classifier confidence
        }
    """
    args = parser.parse_args()
    image_path = current_app.root_path + '\\static\\tmp\\' + args['image_name']
    print(image_path)
    Image.open(image_path)

    try:
        img = Image.open(image_path)

        classifier_name = args['classifier']
        for index in range(len(pretrained_classifiers)):
            if pretrained_classifiers[index].name.strip() == classifier_name:
                classifier_id = index
                break
        _, label = predict(img, classifier_id)
    except IndexError:
        classifiers_blueprint.abort(404)
    except ValueError:
        classifiers_blueprint.abort(422)

    return json.dumps({
        "flag": True,
        "data": [
            {"index": elem[0].item(),
             "label": elem[1],
             "percentage": elem[2]} for elem in label]
    })


def predict(image, classifier_index, scale=1):
    """Return the prepared image and the prediction.
    """
    classifier = pretrained_classifiers[int(classifier_index)].classifier
    return classifier.get_image(image, scale), classifier.predict(image)
