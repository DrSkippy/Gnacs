from distutils.core import setup

GNACS_VERSION_NUMBER = "0.7.6"

if '__main__' == __name__:
    setup(
        name='gnacs',
        version=GNACS_VERSION_NUMBER,
        author='Scott Hendrickson, Josh Montague, Jinsub Hong, Jeff Kolb, Brian Lehman',
        author_email='scott@drskippy.net',
        packages=['acscsv'],
        scripts=['gnacs.py'],
        url='https://github.com/DrSkippy27/Gnacs',
        download_url='https://github.com/DrSkippy27/Gnacs/tags/%s'%(GNACS_VERSION_NUMBER),
        license='LICENSE.txt',
        description='Gnip normalized activity JSON to csv parser (Disqus Comments, Wordpress, Twitter, Tumblr, Foursquare, StockTwits)',
        install_requires=[
                    "ujson >= 1.2",
                        ]
        )
