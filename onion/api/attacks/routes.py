from flask import Blueprint
import json
from onion.api.attacks.models import attacks


attacks_blueprint = Blueprint('attacks', __name__)


@attacks_blueprint.route('/attacks', methods=['GET', 'POST'])
def get_attacks():
    """Get a list of all the attacks.

    Return
    -------
    List of JSON, where
        every JSON has the form
        {
            "name": attack name,
            "paper": attack research paper
        }
    """
    return json.dumps({
        "flag": True,
        "data": [{
            "name": attack["name"],
            "paper": attack["paper"]
        } for attack in attacks]
    })
