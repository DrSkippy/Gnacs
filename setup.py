from distutils.core import setup

setup(
    name='diacs',
    version='0.2.0',
    author='Scott Hendrickson',
    author_email='scott@drskippy.net',
    packages=['diacscsv', 'wpacscsv', 'reflect'],
    scripts=['diacs.py','gnacs-prettifier.py', 'gnacs.py'],
    url='http://pypi.python.org/pypi/diacs/',
    license='LICENSE.txt',
    description='Gnip normalized Disqus comment and Wordperfect post JSON activity to csv parser.',
    long_description=open('README.txt').read(),
    install_requires=[
        "ujson >= 1.2",
    ],
)
