## Gnip Normalized Activities Parser

``gnacs`` parses JSON-formatted activity streams from Gnip's [data APIs](http://gnip.com/products/) and outputs delimited, ordered fields (csv-like). Command-line options allow for some customization of the output, and a framework for more involved extensions is outlined below. It also includes a thin handler for terms of service compliance. 

The most recent version of the auto-generated documentation for the code available on PyPI is visible is visible via [the gh-pages branch](http://drskippy.github.io/Gnacs/) (*note:* these docs are currently a work-in-progress - stay tuned!). 
  

### Installation

``gnacs`` is a available on [PyPI](https://pypi.python.org/pypi/gnacs/) in a tarball, or can be ``pip install``'d:

If you have a `C` complier installed (e.g. gcc, or Xcode on OS X):

    $ sudo pip install gnacs 
    $ sudo pip install gnacs --upgrade   # if you've installed before

If you don't have a `C` complier:

     $ sudo pip install gnacs --no-deps 
     $ sudo pip install gnacs --no-deps --upgrade   # if you've installed before

(Or the ``sudo``-less equivalent, if you're using a ``virtualenv``).


### Usage

``gnacs`` is commonly used in one of two manners: either as a command-line utility (works with ``stdin`` and ``stdout``), or as imported modules within other Python code. Supported data sources: 

- Twitter
- Disqus
- Wordpress

The default output (no cmd-line options) will work with input data from any of these sources. The ``-z`` option (must be the last option) takes the source (aka "publisher") as an argument. 

    $ ./gnacs.py -h
    usage: gnacs.py [-h] [-a] [-g] [-i] [-c] [-l] [-j] [-o] [-p] [-s] [-t] [-r]
                    [-u] [-v] [-x] [-z PUB] [-k KEYPATH]
                    [file_name]

    Parse seqeunce of JSON formated activities.

    positional arguments:
      file_name             Input file name (optional).

    optional arguments:
      -h, --help            show this help message and exit
      -a, --status          Version, status, etc.
      -g, --geo             Include geo fields
      -i, --influence       Show user's influence metrics
      -c, --csv             Comma-delimited output (, default is | without quotes)
      -l, --lang            Include language fields
      -j, --geojson         Output is geojson format (Foursquare and Twitter only)
                            Caution: dataset must fit in memory.
      -o, --origin          Include source/origin fields
      -p, --pretty          Pretty JSON output of full records
      -s, --urls            Include urls fields
      -t, --structure       Include thread linking fields
      -r, --rules           Include rules fields
      -u, --user            Include user fields
      -v, --version         Show version number
      -x, --explain         Show field names in output for sample input records
      -z PUB, --publisher PUB
                            Publisher (default is twitter), twitter,
                            disqus, wordpress, wpcomments
      -k KEYPATH, --keypath KEYPATH
                            returns a value from a path of the form 'key:value'

For exact payload values returned by the various options, you can dig into the code in ``acscsv/``; modules are named with a ``<source>_acs.py`` convention.  


A handful of sample data files are found in ``data/`` for experimentation. Some examples of usage: 

**"Prettify" JSON**

    $ ./gnacs.py -p data/tumblr.sample.json 
    {
    "tumblrRebloggedFrom": {
       "link": "http://illllest.tumblr.com/post/45832750088", 
          "author": {
             "displayName": "Unknown Pleasures", 
             "link": "http://illllest.tumblr.com/"
          }
    }, 
    "target": {
          "displayName": "stardustgrass", 
          "link": "http://stardustgrass.tumblr.com/", 
          "objectType": "blog"
    }, 
    "gnip": {}, 
    "object": {
      "tumblrNoteCount": 303949, 
      "tumblrReblogKey": "57dc6dOl", 
      "objectTypes": [
           "image"
      ], 
    ...

**Include the user, language, and structure (activity connections) options, while specifying that the input data is from Disqus** 


    $ cat data/disqus_sample.json | ./gnacs.py -ultz disqus
    tag:gnip.disqus.com:2012:comment/hosqas/post/2013-03-19T08:30:38|2013-03-19T12:30:38+00:00|So Bush, Cheney and oil cartels did something for US after all these wars and massacres.|en|5gat|4okb2q|http://cnnpreview.turner.com:82/interactive/2013/03/world/baby-noor/index.html|hoit02|uivnl|rvd3a
    tag:gnip.disqus.com:2012:comment/honzhg/update/2013-03-18T19:31:47/b11a0781c2f4d7497c28b948a05c586d30bf986ad19dbca50c17201cd9cf57aa|2013-03-18T23:31:47+00:00|Yes, I agree. The concept of the book sounded interesting and then the review was wholly disappointing. Although this argument above is really juvenile,  I have to give it credit for being more interesting than the review.|en|t3dj|4ing01|http://www.avclub.com/articles/alexander-theroux-the-grammar-of-rock-art-and-artl,93788/|hoviki|lvns6|ytar7
    tag:gnip.disqus.com:2012:comment/hosqcb/post/2013-03-19T08:30:42|2013-03-19T12:30:42+00:00|Traitre|None|aasak|403pb5|http://www.eurosport.fr/football/premier-league/2012-2013/michael-owen-prend-sa-retraite_sto3673680/story.shtml|None|None|j2qov
    tag:gnip.disqus.com:2012:comment/hjkqvk/update/2013-03-17T17:55:59/73137b5b41df0a1e51183774150849b5a0c90d81b095378ac72309a43b26994f|2013-03-17T21:55:59+00:00|@Lô el Magnifico oui zen cool !|es|aasak|43t8by|http://www.eurosport.fr/formule-1/grand-prix-d-australie/2013/photos-les-girlfriends-des-pilotes-de-f1_sto3671086/story.shtml|hjk4l0|960y6|9s241
    ...

**GeoJSON output from Foursquare data**

The ``-j`` option will process activities with geo-coordinates (all Foursquare activities, and geo-tagged Twitter activities) and output a [GeoJSON-compliant](http://geojson.org/geojson-spec.html) data structure. This is particularly convenient for posting to a [gist](https://gist.github.com/jrmontag/9980ee3f79154ec81bff) or anywhere on [GitHub](data/twitter_sample.geojson), where it is magically rendered into the corresponding map. 

    $ ./gnacs.py -jz fsq data/foursquare_sample.json 
    {type: "FeatureCollection", features: [{geometry: {type: "Point",coordinates: [-101.0379045,47.29088246]}
    ...


### Customized output

*Note:* this section is currently only applicable to Activity Streams data from Twitter.

One of the goals of ``gnacs`` is to make easy the programmatic creation of delimited output of user-specified fields from the Activity Streams payloads. Below is a workflow for extending the existing framework to create custom output without modifying the core code.  

To start working on your custom output, pull the most recent changes to ``master`` - likely from [DrSkippy's remote](https://github.com/DrSkippy/Gnacs) - and make a new branch for yourself. 

    $ git checkout master           # if you're not already on it
    $ git pull upstream master      # assumes you've set it to DrSkippy 
    $ git branch my-new-branch      # or something more descriptive 

This new branch will likely contain all of your custom output, in the form of new modules. On your new branch, go into the ``acscsv`` directory, and copy the ``custom_output.py`` module to something that relates to your new output use-case, and open it up to edit.

    $ cp custom_output.py 2014-06_new-output.py    # again, descriptive is good 

This module imports all the necessary machinery for using the core ``gnacs`` code, but exposes the method that specifies the output. Your new custom output module has a few lines of example code which you can delete or edit. The ordering of fields in this list determines the order in the delimited output. The fields (and their values) are identified by the classes defined in the [twitter_acs_fields.py](acscsv/twitter_acs_fields.py) module. The class names are ``Field_`` followed by the set of keys used to obtain the final value. For many uses, this method may be the only thing you need to edit.

For more complicated processing, you can also add new classes at the top of the module. For example, these could inherit from the standard ones in ``twitter_acs_fields.py`` and then modify the values. See, for example, the [custom MySQL module in the JM branch](https://github.com/jrmontag/Gnacs/blob/JM/acscsv/2014-06_mysql.py). 

Your new modules uses almost exactly the same file input methods as the core ``gnacs`` code. To test your new module, pass the Twitter sample JSON data through your new module (make it executable if it's not already). For example, using the ``custom_output.py`` template that comes in ``master``:

    $ cat ~/Gnacs/data/twitter_sample.json | ./custom_output.py 
    TR|351835317671690241|uykugibisiyok|None
    US|351835317604593666|CoBerg_|[47.29088246, -101.0379045]
    JP|351835317747191808|yamasyoyamasyo|[35.70675048, 139.84273005]

The one exception to the file reading is that the custom module does not currently play nice with closed shell pipes (e.g. ``cat bigfile | ./my-new-output.py | head`` will crash with a closed pipe error). This will be resolved at a later date. 

Keep your branch and all of it's custom, one-off modules around as long as you need, or delete it whenever you like. By keeping an eye on the ``master`` branch, you can benefit from core code changes by simply cherrypicking the modules as needed. For example, if a new, extremely valuable functionality is added to the core ``acscsv.py`` module, you can do something like the following to get your fork up to speed...  

    $ git checkout master               
    $ git pull upstream remote                  # get upstream change from DrSkippy again
    $ git checkout my-new-branch 
    $ git checkout master acscsv/acscsv.py      # checkout from the branch on your own fork 
    # ... commit & push everything back to GitHub
 
The number of steps involved in that last step will depend on how your ``.gitconfig`` is set up.


### Contribution 

If you would like to contribute code to the core ``gnacs`` code, feel free to fork the project and add your awesome new features. 

**Testing**

When you add new features (or whenever you're feeling inspired by the test gods), add to the existing test coverage (see the ``test_*`` modules within ``acscsv/`` for some starting points). Ideally, your tests follow the ``unittest`` paradigm and are picked up by the current test framework. To run all the tests, go to the repo base and run:

    $ make tests 




--------------------------

coming soon: 

- doc generation & instructions

``sudo pip install sphinx autodoc ghp-import sphinx-argparse``

