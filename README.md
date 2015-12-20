### What is it?:

A python script to change my desktop wallpaper picked from reddit.

### Scope: 

* [x] Must only fetch 1920x1080 pixel images.
* [x] Looks from a list of definied subbredits. (uses public MultiReddits)
* [ ] Maintains a list of previously used wallpapers to avoid duplicates.

### Requirements:

* Unity/Gnome Shell 3
* Python 3+ : sudo apt-get install python3
* [requests](http://docs.python-requests.org/en/latest/) : pip3 install requests
* [praw](https://praw.readthedocs.org/en/stable/) : pip3 install praw

### TO Do's

* Make use of configuration files to get subbredit list/multireddit/username.
* Store a hash of previously used images, to avoid duplicates.