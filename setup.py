from distutils.core import setup

setup(
    name='gnacs',
    version='0.3.6',
    author='Scott Hendrickson',
    author_email='scott@drskippy.net',
    packages=['diacscsv', 'wpacscsv', 'reflect', 'twacscsv', 'tblracscsv'],
    scripts=['diacs.py','gnacs-prettifier.py', 'gnacs.py', 'twacs.py'],
    url='http://pypi.python.org/pypi/diacs/',
    license='LICENSE.txt',
    description='Gnip normalized activity JSON to csv parser (Disqus Comments, Wordpress, Twitter, Tumblr)',
    long_description=open('README.txt').read(),
    install_requires=[
        "ujson >= 1.2",
    ],
)
