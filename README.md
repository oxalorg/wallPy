### What is it?:

A python script to change my desktop wallpaper picked from reddit.

### Scope:

* [x] Must only fetch 1920x1080 pixel images. (Implemented in v0.0.1)
* [x] Looks from a list of definied subbredits. (uses public MultiReddits) (Implemented in v0.0.1)
* [x] Maintains a list of previously used wallpapers to avoid duplicates. (Implemented in v0.0.2)

### Requirements:

* Unity/Gnome Shell 3
* Python 3+ : sudo apt-get install python3
* [requests](http://docs.python-requests.org/en/latest/) : pip3 install requests
* [praw](https://praw.readthedocs.org/en/stable/) : pip3 install praw


### Installing

You can find the latest release [here](https://github.com/MiteshNinja/wallPy/releases/latest).  
Use master branch for development purposes only.

```shell
# cd to directory where you want to install
cd ~/.apps
wget https://github.com/MiteshNinja/wallPy/archive/v0.0.2.tar.gz
tar -zxvf wallPy-0.0.2.tar.gz
cd wallPy-0.0.2
```

Now you can use virtualenv to install required packages locally.

```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Now run the app

```
python3 wallPy.py
```

I'll soon be uploading to pypi so that all this mess can be avoided. Bare with me till then.

### TO Do's

* [ ] Upload to PyPI
* [ ] Make use of configuration files to get subbredit list/multireddit/username.
* [x] Store a hash of previously used images, to avoid duplicates. (Implemented in v0.0.2)
