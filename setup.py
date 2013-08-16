from distutils.core import setup

setup(
    name='gnacs',
    version='0.7.0',
    author='Scott Hendrickson, Josh Montague, Jinsub Hong',
    author_email='scott@drskippy.net',
    packages=['acscsv'],
    scripts=['stntv.py', 'wpacs.py', 'ggacs.py','tblracs.py', 'diacs.py', 'gnacs.py', 'twacs.py', 'fsqacs.py'],
    url='https://github.com/DrSkippy27/Gnacs',
    download_url='https://github.com/DrSkippy27/Gnacs/tags/0.6.9',
    license='LICENSE.txt',
    description='Gnip normalized activity JSON to csv parser (Disqus Comments, Wordpress, Twitter, Tumblr, Foursquare, GetGlue, StockTwits)',
    install_requires=[
                "ujson >= 1.2",
                    ]
    )
