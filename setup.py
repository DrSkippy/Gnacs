from distutils.core import setup

GNACS_VERSION_NUMBER = "0.7.6"

setup(
    name='gnacs',
    version=GNACS_VERSION_NUMBER,
    author='Scott Hendrickson, Josh Montague, Jinsub Hong, Jeff Kolb, Brian Lehman',
    author_email='scott@drskippy.net',
    packages=['acscsv'],
    scripts=['ngacs.py', 'stntv.py', 'wpacs.py', 'ggacs.py','tblracs.py', 'diacs.py', 'gnacs.py', 'twacs.py', 'fsqacs.py'],
    url='https://github.com/DrSkippy27/Gnacs',
    download_url='https://github.com/DrSkippy27/Gnacs/tags/%s'%(GNACS_VERSION_NUMBER),
    license='LICENSE.txt',
    description='Gnip normalized activity JSON to csv parser (Disqus Comments, Wordpress, Twitter, Tumblr, Foursquare, GetGlue, StockTwits)',
    install_requires=[
                "ujson >= 1.2",
                    ]
    )
