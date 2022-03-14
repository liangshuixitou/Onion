from flask import Blueprint
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
