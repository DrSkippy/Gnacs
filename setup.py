from distutils.core import setup

setup(
    name='gnacs',
    version='0.4.0',
    author='Scott Hendrickson, Josh Montague',
    author_email='scott@drskippy.net',
    packages=['diacscsv', 'wpacscsv', 'reflect', 'twacscsv', 'tblracscsv', 'fsqacscsv'],
    scripts=['tblracs.py', 'diacs.py','gnacs-prettifier.py', 'gnacs.py', 'twacs.py', 'fsqacs.py'],
    url='http://pypi.python.org/pypi/gnacs/',
    license='LICENSE.txt',
    description='Gnip normalized activity JSON to csv parser (Disqus Comments, Wordpress, Twitter, Tumblr, Foursquare)',
    long_description=open('README.md').read(),
    install_requires=[
        "ujson >= 1.2",
    ],
)
