import subprocess
import sys
import requests
import praw
import sluggerNinja
import hashNinja
import warnings

r = praw.Reddit(user_agent = "linux:wallPy:v0.0.1 (by /u/MiteshNinja)")


def supress_warnings(func):
    def f(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)
    return f


@supress_warnings
def get_image_url(post):
    """ Get the image url from MultiReddit post object """
    if not post.is_self and not post.over_18:
        img_ht = post.preview['images'][0]['source']['height']
        img_wt = post.preview['images'][0]['source']['width']
        if img_ht > 1000 and img_wt > 1900 and (1.7-0.4) <= (img_wt/img_ht) <= (1.7+0.4):
            return post.preview['images'][0]['source']['url']
    else:
        print("[ ] " + str(post.score) + " :: " + post.title)
    return False

@supress_warnings
def get_image(post, image_url):
    """ Download image to file from the specified image_url"""
    try:
        req = requests.get(image_url)
        req.raise_for_status()
        image_slug = '/home/mitesh/Pictures/Wallpapers/' + sluggerNinja.slugify(post.title)
        image_file = open(image_slug, 'wb')
        for chunk in req.iter_content(100000):
            image_file.write(chunk)
        return image_slug
    except:
        # print(sys.exc_info()[0])
        return False
    finally:
        image_file.close()
        req.close()

@supress_warnings
def add_image_hash(image_hash):
    """ Add hash of the finalized image file to .prevImages.log """
    prevImages_file = open('./.prevImages.log', 'a')
    prevImages_file.write(image_hash + '\n')
    prevImages_file.close()

@supress_warnings
def search_prevImages(image_hash):
    """ Search previously used images for a match with currently fetched image"""
    with open('./.prevImages.log', 'r') as f:
        for line in f:
            if line[:-1] == image_hash:
                return True
        return False

@supress_warnings
def main():
    image_set = False
    submissions = r.get_multireddit('MiteshNinja', 'wallpaper_generic').get_hot()

    while not image_set:
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
            print("[X] " + str(post.score) + " :: " + post.title)


if __name__ == '__main__':
    # To make sure a file exists.
    open('./.prevImages.log', 'a').close()
    main()