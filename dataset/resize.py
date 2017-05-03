from os import listdir
from os.path import join, isfile, isdir
from typing import Tuple

from PIL import Image
from resizeimage import resizeimage

from dataset.shared import maybe_create_folder


class ImagenetResizer:
    def __init__(self, source_dir: str, dest_dir: str):
        if not isdir(source_dir):
            raise Exception('Input folder does not exists: {}'
                            .format(source_dir))
        self.source_dir = source_dir

        # Destination folder
        maybe_create_folder(dest_dir)
        self.dest_dir = dest_dir

    def resize_img(self, filename: str, size: Tuple[int, int] = (299, 299)):
        """
        Resizes the image using padding
        :param filename:
        :param size:
        """
        img = Image.open(join(self.source_dir, filename))
        cover = resizeimage.resize_contain(img, size)
        cover.save(join(self.dest_dir, filename), 'JPEG')

    def resize_all(self, size=(299, 299)):
        for filename in listdir(self.source_dir):
            if isfile(join(self.source_dir, filename)):
                self.resize_img(filename, size)


# Run from the top folder as:
# python3 -m dataset.resize <args>
if __name__ == '__main__':
    import argparse
    from dataset.shared import dir_originals, dir_resized

    # Argparse setup
    parser = argparse.ArgumentParser(
        description='Resize images from a folder to 299x299')
    parser.add_argument('-s', '--source-folder',
                        default=dir_originals,
                        type=str,
                        metavar='FOLDER',
                        dest='source',
                        help='use FOLDER as source of the images (default: {})'
                        .format(dir_originals))
    parser.add_argument('-o', '--output-folder',
                        default=dir_resized,
                        type=str,
                        metavar='FOLDER',
                        dest='output',
                        help='use FOLDER as destination (default: {})'
                        .format(dir_resized))

    args = parser.parse_args()
    ImagenetResizer(args.source, args.output).resize_all((299, 299))
