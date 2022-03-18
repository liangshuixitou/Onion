from flask import Blueprint
import os
import secrets
from flask import current_app, request
from PIL import Image
import PIL

images_blueprint = Blueprint('images', __name__)


@images_blueprint.route('/save', methods=['GET', 'POST'])
def save_image():
    """Compress and save user-uploaded images to the filesystem.

    Returns
    -------
    [image_fn]
        File name of resized image as it is saved on filesystem.
    """
    source_image = request.files.get('file')
    path = 'tmp'
    output_size = (125, 125)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(source_image.filename)

    if not f_ext:
        # This is in case a PIL image or
        # some buffer data was passed.
        f_ext = ".jpg"

    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path,
                              'static/' + path,
                              image_fn)

    i = compress_image(source_image, output_size)
    i.save(image_path)

    return image_fn


def compress_image(image, output_size=(125, 125)):
    """Compress input image.

    Parameters
    ----------
    image : [image]
        Any valid image.
    output_size : tuple, optional
        Desired output size, default is (125, 125).

    Returns
    -------
    [i]
        Compressed image.
    """
    if isinstance(image, PIL.ImageFile.ImageFile):
        i = image
    else:
        i = Image.open(image)

    i.thumbnail(output_size)
    return i
