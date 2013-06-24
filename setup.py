from distutils.core import setup

setup(
    name='gnacs',
    version='0.5.0',
    author='Scott Hendrickson, Josh Montague',
    author_email='scott@drskippy.net',
    packages=['ggacscsv','diacscsv', 'wpacscsv', 'reflect', 'twacscsv', 'tblracscsv', 'fsqacscsv'],
    scripts=['wpacs.py','ggacs.py','tblracs.py', 'diacs.py','gnacs-prettifier.py', 'gnacs.py', 'twacs.py', 'fsqacs.py'],
    url='https://github.com/DrSkippy27/Gnacs',
    download_url='https://github.com/DrSkippy27/Gnacs/tags/4.0.3',
    license='LICENSE.txt',
    description='Gnip normalized activity JSON to csv parser (Disqus Comments, Wordpress, Twitter, Tumblr, Foursquare, GetGlue)',
    install_requires=[
        "ujson >= 1.2",
    ],
)
