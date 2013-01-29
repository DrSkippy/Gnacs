from distutils.core import setup

setup(
    name='diacs',
    version='0.1.2',
    author='Scott Hendrickson',
    author_email='scott@drskippy.net',
    packages=['diacscsv'],
    scripts=['diacs.py','diacs-prettifier.py'],
    url='http://pypi.python.org/pypi/diacs/',
    license='LICENSE.txt',
    description='Gnip normalized Disqus JSON activity to csv parser.',
    long_description=open('README.txt').read(),
    install_requires=[
        "ujson >= 1.2",
    ],
)
