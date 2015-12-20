import subprocess
import sys
import requests
import praw
import sluggerNinja

r = praw.Reddit(user_agent = "linux:wallPy:v0.0.1 (by /u/MiteshNinja)")


def get_image_url(post):
    if not post.is_self and not post.over_18:
        if post.preview['images'][0]['source']['height'] > 1000 and post.preview['images'][0]['source']['width'] > 1900:
            print(post)
            return post.preview['images'][0]['source']['url']
    return False


def get_image(post, image_url):
    try:
        req = requests.get(image_url)
        req.raise_for_status()
        image_slug = '/home/mitesh/Pictures/Wallpapers/' + sluggerNinja.slugify(post.title)
        image_file = open(image_slug, 'wb')
        for chunk in req.iter_content(100000):
            image_file.write(chunk)
        return image_slug
    except:
        print(sys.exc_info()[0])
        return False
    finally:
        image_file.close()


def main():
    image_set = False
    lmt = 10
    submissions = r.get_multireddit("MiteshNinja", "wallpaper_generic").get_hot(limit=lmt)
    while not image_set:
        post = next(submissions)
        image_url = get_image_url(post)
        if not image_url:
            continue
        image_file_uri = get_image(post, image_url)
        if not image_file_uri:
            continue
        set_wallpaper_cmd = 'gsettings set org.gnome.desktop.background picture-uri file://' + image_file_uri
        return_code = subprocess.call(set_wallpaper_cmd, shell=True)
        image_set = True
        if return_code:
            print("Error setting the image as wallpaper.")
            image_set = False


if __name__ == "__main__":
    main()