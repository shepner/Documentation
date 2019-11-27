This all originated from [here](https://gist.github.com/coleifer/d93d6c43e59698d149c0):

* [a little note-taking app with Flask](http://charlesleifer.com/blog/saturday-morning-hack-a-little-note-taking-app-with-flask/)
* [Revisiting the notes app](http://charlesleifer.com/blog/saturday-morning-hacks-revisiting-the-notes-app/)
* [Adding full-text search to the flask note-taking app](http://charlesleifer.com/blog/saturday-morning-hacks-adding-full-text-search-to-the-flask-note-taking-app/)

installation:
``` shell
sudo -H pip3 install flask
sudo -H pip3 install huey
sudo -H pip3 install micawber
sudo -H pip3 install peewee
sudo -H pip3 install redis
sudo -H pip3 install markdown
sudo -H pip3 install flask_peewee
sudo -H pip3 install beautifulsoup4
```

install the app itself:

``` shell
wget https://gist.github.com/coleifer/d93d6c43e59698d149c0/archive/61b506deaa43883e819dc20a01ca22547440835e.zip
unzip 61b506deaa43883e819dc20a01ca22547440835e.zip
cp d93d6c43e59698d149c0-61b506deaa43883e819dc20a01ca22547440835e/* .
rm 61b506deaa43883e819dc20a01ca22547440835e.zip
rm -R d93d6c43e59698d149c0-61b506deaa43883e819dc20a01ca22547440835e
```


[Bootstrap](https://getbootstrap.com/):

``` shell
wget https://github.com/twbs/bootstrap/releases/download/v3.1.1/bootstrap-3.1.1-dist.zip
unzip bootstrap-3.1.1-dist.zip
mkdir static
mv bootstrap-3.1.1-dist/* static/
rm -R bootstrap-3.1.1-dist
```


try this later:

``` shell
wget https://github.com/twbs/bootstrap/releases/download/v4.4.0/bootstrap-4.4.0-dist.zip
unzip bootstrap-4.4.0-dist.zip
mkdir static
mv bootstrap-4.4.0-dist/* static/
rm -R bootstrap-4.4.0-dist
```


[superhero theme](https://bootswatch.com/superhero/)

``` shell
wget static/css https://bootswatch.com/4/superhero/bootstrap.css
wget https://bootswatch.com/4/superhero/bootstrap.min.css
mv bootstrap* static/css
```


More JS that needs to be installed:

``` shell
#jQuery
wget -P static/js http://code.jquery.com/jquery-1.11.0.min.js
#imagesloaded
wget -P static/js http://imagesloaded.desandro.com/imagesloaded.pkgd.min.js
#masonry
wget -P static/js http://masonry.desandro.com/masonry.pkgd.min.js
```


From the distro, you must move the `templates.*` files to ``./templates/`` and remove the `template.` prefix from the names.  [This](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates) was helpful for providing that insight.  Similar for statis.js.notes.js:

``` shell
mkdir templates
cp templates.homepage.html templates/homepage.html
cp templates.note.html templates/note.html

cp static.js.notes.js static/js/notes.js
```
