import subprocess
import sys
import requests
import praw
import sluggerNinja
import hashNinja
import warnings
import logging

img_checked = 0
config = {'MIN_IMG_HT': 800, 'MIN_IMG_WT': 800, 'NSFW': False}

r = praw.Reddit(user_agent="linux:wallPy:v0.0.2 (by /u/MiteshNinja)")
logging.basicConfig(filename="./wallPy_temp.log",
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')


def supress_warnings(func):
    def f(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return f


def progress_output(post, final_img):
    if final_img:
        print("Total images checked: {}".format(img_checked - 1))
        print("Selected image details:")
        print(post)
    print("{:->4}".format(post.score) + " :: " + post.title)
    print("Images checked: {}\033[F".format(img_checked - 1), end='')


def get_image_url(post):
    """ Get the image url from MultiReddit post object """
    if not post.is_self and not (False if config['NSFW'] else post.over_18):
        img_ht = post.preview['images'][0]['source']['height']
        img_wt = post.preview['images'][0]['source']['width']
        if img_ht > config['MIN_IMG_HT'] and img_wt > config[
                'MIN_IMG_WT'] and (1.7 - 0.6) <= (img_wt / img_ht) <= (
                    1.7 + 0.6):
            return post.preview['images'][0]['source']['url']
        else:
            progress_output(post, False)
    return False


def get_image(post, image_url):
    """ Download image to file from the specified image_url"""
    try:
        s = requests.Session()
        req = s.get(image_url)
        req.raise_for_status()
        image_slug = '/home/ox/Pictures/Wallpapers/' + sluggerNinja.slugify(
            post.title)
        image_file = open(image_slug, 'wb')
        for chunk in req.iter_content(100000):
            image_file.write(chunk)
        image_file.close()
        return image_slug
    except Exception as e:
        print(e)
        print('Some error while getting image')
        return False
    finally:
        s.close()


def add_image_hash(image_hash):
    """ Add hash of the finalized image file to .prevImages.log """
    prevImages_file = open('./.prevImages.log', 'a')
    prevImages_file.write(image_hash + '\n')
    prevImages_file.close()


def search_prevImages(image_hash):
    """ Search previously used images for a match with currently fetched image"""
    with open('./.prevImages.log', 'r') as f:
        for line in f:
            if line[:-1] == image_hash:
                return True
        return False


def main():
    image_set = False
    submissions = r.get_multireddit('MiteshNinja',
                                    'wallpaper_generic').get_hot(limit=None)
    while not image_set:
        try:
            global img_checked
            img_checked += 1
            post = next(submissions)
            image_url = get_image_url(post)
            if not image_url:
                continue
            image_file_uri = get_image(post, image_url)
            if not image_file_uri:
                continue

            image_hash = hashNinja.md5hash(image_file_uri)
            # Search if this image has been used before
            if search_prevImages(image_hash):
                continue

            set_wallpaper_cmd = "gsettings set org.gnome.desktop.background picture-uri file://" + image_file_uri
            return_code = subprocess.call(set_wallpaper_cmd, shell=True)
            if return_code:
                print("Error setting the image as wallpaper.")
                image_set = False
            else:
                add_image_hash(image_hash)
                image_set = True
                progress_output(post, True)
                return True
        except KeyboardInterrupt:
            print('Exiting...')
            return False


if __name__ == '__main__':
    # To make sure a file exists.
    open('./.prevImages.log', 'a').close()
    main()
