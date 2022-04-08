from PIL import Image
import os


def watermark_with_transparency(input_image_path, output_image_path, watermark_image_path):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    width, height = base_image.size
    _w, _h = watermark.size
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (0, height - _h), mask=watermark)
    transparent.save(output_image_path)


if __name__ == '__main__':

    # checking for exists logo
    if not os.path.exists('./logo.png'):
        print("-- Error: 'logo.png' not found !")
        exit()

    # datas
    publish_flag = False
    publish_dir_path = "./#_publish/"
    black_list = ["logo.png", "run.py"]
    valid_extensions = [".png", ".jpg", ".jpeg", ".gif"]

    for filename in os.scandir('.'):

        # checking if it is a file
        if filename.is_file():
            # checking for validations
            _check = all(map(lambda x: x not in filename.path, valid_extensions)) or \
                     any(filter(lambda x: x in filename.path, black_list))
            if _check:
                print(f"-- ignore: {filename.path[2:]}")
                continue

            # checking if exists output directory
            if not publish_flag:
                if not os.path.exists(publish_dir_path):
                    os.mkdir(publish_dir_path)
                publish_flag = True

            # Start process :
            img = filename.path
            watermark_with_transparency(img, f"{publish_dir_path}{filename.path[2:]}", 'logo.png')

            print(f"'{img[2:]}' - completed .")
