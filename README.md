# Gnacs

## Gnip Normalized Activities Parser

Parses JSON activity sterams from Gnip straming APIs (Powertrack, Historical, Search API)
and provides delimited, ordered fields as output.  Extended options allow multi-file output
approprite for loading into a relational database or GeoJSON output appropriate for
immediat rendering on e.g. github.com.


### Install
If you have a `c` complier installed (e.g. gcc, or Xcode on OS X):

    `sudo pip install gnacs` 
    `sudo pip install gnacs --upgrade` (if you have installed before)

If you don't have a c complier:

     `sudo pip install gnacs --no-deps` 
     `sudo pip install gnacs --no-deps --upgrade` (if you have installed before)

In order to regenerate the documentation, you will need:

     `sudo pip install sphinx autodoc ghp-import sphinx-argparse` 

To view the Sphinx docs go [here](https://drskippy27.github.io/Gnacs/)

### Supported publishers:
* Twitter
* Disqus
* Wordpress
* Tumblr
* Foursquare 
* Stocktwits 

### Usage ###
> ./gnacs.py -h
usage: gnacs.py [-h] [-a] [-g] [-i] [-c] [-l] [-j] [-o] [-p] [-s] [-t] [-r]
                [-u] [-v] [-x] [-z PUB] [-k KEYPATH] [-D]
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
                        Publisher (default is twitter), twitter, newsgator,
                        disqus, wordpress, wpcomments, tumblr, foursquare,
                        getglue, stocktwits, stocktwits-native
  -k KEYPATH, --keypath KEYPATH
                        returns a value from a path of the form 'key:value'
  -D, --database        directs stdout to file objects for uploading to mysql
                        db tables

### Use Examples ###
Sample files are included in the data directory, for example:

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


    $ ./gnacs.py -z twitter data/twitter_sample.json 
    tag:search.twitter.com,2005:291929508213297153|2013-01-17T15:26:33.000Z|@derryghirl as nana would say " she's deit-it "
    tag:search.twitter.com,2005:309063808016584704|2013-03-05T22:12:08.000Z|Giving them 1 inch and they take a mile
    tag:search.twitter.com,2005:309063807509094400|2013-03-05T22:12:08.000Z|Imperialihmo, como decía él.
    tag:search.twitter.com,2005:309063808234700802|2013-03-05T22:12:08.000Z|動画をツイッター上であんまり勧めることがないあてくし。だがしかーし！！！！観てくれ聴いてくれ！！！！
    tag:search.twitter.com,2005:309063808142434305|2013-03-05T22:12:08.000Z|SON DAKİKA : Manchester'da olay! İngilizler kebap salonuna saldırdı! http://t.co/eW8XDwlCtc
    tag:search.twitter.com,2005:309063808129835008|2013-03-05T22:12:08.000Z|Mi mas sentido pésame para los familiares del Presidente Chávez y para todos sus seguidores. Q.E.P.D
    ...

    $ ./gnacs.py data/twitter_sample.json.gz -z twitter 
    tag:search.twitter.com,2005:351835320817426433|2013-07-01T22:50:51.000Z|Como cuando grito ¡¡*José*!! y la mayoria de mis primos voltea ...
    tag:search.twitter.com,2005:351835321006170112|2013-07-01T22:50:51.000Z|Tweeting for no reason
    tag:search.twitter.com,2005:351835321056509952|2013-07-01T22:50:51.000Z|And I'm the one that always gets hit on. OKAAAAY.
    tag:search.twitter.com,2005:351835320297328640|2013-07-01T22:50:51.000Z|@CheniseFowlisX yeah 😂
    tag:search.twitter.com,2005:351835321220075524|2013-07-01T22:50:52.000Z|@justinbagdr no, non mi far star meglio.
    tag:search.twitter.com,2005:351835321471746048|2013-07-01T22:50:52.000Z|😕 Hmm...
    ...


    $ cat data/disqus_sample.json | ./gnacs.py -z disqus -ult
    tag:gnip.disqus.com:2012:comment/hosqas/post/2013-03-19T08:30:38|2013-03-19T12:30:38+00:00|So Bush, Cheney and oil cartels did something for US after all these wars and massacres.|en|5gat|4okb2q|http://cnnpreview.turner.com:82/interactive/2013/03/world/baby-noor/index.html|hoit02|uivnl|rvd3a
    tag:gnip.disqus.com:2012:comment/honzhg/update/2013-03-18T19:31:47/b11a0781c2f4d7497c28b948a05c586d30bf986ad19dbca50c17201cd9cf57aa|2013-03-18T23:31:47+00:00|Yes, I agree. The concept of the book sounded interesting and then the review was wholly disappointing. Although this argument above is really juvenile,  I have to give it credit for being more interesting than the review.|en|t3dj|4ing01|http://www.avclub.com/articles/alexander-theroux-the-grammar-of-rock-art-and-artl,93788/|hoviki|lvns6|ytar7
    tag:gnip.disqus.com:2012:comment/hosqcb/post/2013-03-19T08:30:42|2013-03-19T12:30:42+00:00|Traitre|None|aasak|403pb5|http://www.eurosport.fr/football/premier-league/2012-2013/michael-owen-prend-sa-retraite_sto3673680/story.shtml|None|None|j2qov
    tag:gnip.disqus.com:2012:comment/hjkqvk/update/2013-03-17T17:55:59/73137b5b41df0a1e51183774150849b5a0c90d81b095378ac72309a43b26994f|2013-03-17T21:55:59+00:00|@Lô el Magnifico oui zen cool !|es|aasak|43t8by|http://www.eurosport.fr/formule-1/grand-prix-d-australie/2013/photos-les-girlfriends-des-pilotes-de-f1_sto3671086/story.shtml|hjk4l0|960y6|9s241
    GNIPREMOVE|delete|tag:gnip.disqus.com:2012:comment/hosl5z
    tag:gnip.disqus.com:2012:comment/host4q/update/2013-03-19T08:28:00/9d34ac326ba4c07c6ede2bb9498c31373794ae7c8a495823bd038c86f8045c44|2013-03-19T12:28:00+00:00|These so-called "journalists" remind of this bunch of biddies:  http://www.youtube.com/watch?v=jbhnRuJBHLs|en|i8ey|q221nc|http://newsbusters.org/blogs/tim-graham/2013/03/19/washpost-misleads-catholics-jokes-pope-francis-infallible-man|hos7ya|vjs3d|78ia4
    ...

    $ ./gnacs.py -jz twitter data/twitter_sample.json
    {type: "FeatureCollection", features: [{geometry: {type: "Point",coordinates: [-101.0379045,47.29088246]},type: "Feature",properties: {id: "tag:search.twitter.com,2005:351835317604593666"}},{geometry: {type: "Point",coordinates: [139.84273005,35.70675048]},type: "Feature",properties: {id: "tag:search.twitter.com,2005:351835317747191808"}}, ...


