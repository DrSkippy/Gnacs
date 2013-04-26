from distutils.core import setup

setup(
    name='gnacs',
    version='0.3.0',
    author='Scott Hendrickson',
    author_email='scott@drskippy.net',
    packages=['diacscsv', 'wpacscsv', 'reflect','twacscsv'],
    scripts=['diacs.py','gnacs-prettifier.py', 'gnacs.py'],
    url='http://pypi.python.org/pypi/diacs/',
    license='LICENSE.txt',
    description='Gnip normalized activity JSON to csv parser (Disqus Comments and Wordperfect, Twitter)',
    long_description=open('README.txt').read(),
    install_requires=[
        "ujson >= 1.2",
    ],
)
