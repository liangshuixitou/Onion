from flask import Blueprint
import json
from onion.dao.datasets import datasets

datasets_blueprint = Blueprint('datasets', __name__)


@datasets_blueprint.route('/datasets', methods=['GET', 'POST'])
def get_datasets():
    """Get a list of the names of all datasets in set_datasets.
    """
    return json.dumps({
        "flag": True,
        "data": [{
            "name": dataset['name'],
            "paper": dataset['paper']
        } for dataset in datasets]
    })
