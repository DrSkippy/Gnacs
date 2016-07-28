from distutils.core import setup

GNACS_VERSION_NUMBER = "1.0.1"

if '__main__' == __name__:
    setup(
        name='gnacs',
        version=GNACS_VERSION_NUMBER,
        author='Scott Hendrickson, Josh Montague, Jinsub Hong, Jeff Kolb, Brian Lehman, Fiona Pigott',
        author_email='drskippy@twitter.com',
        packages=['acscsv'],
        scripts=['gnacs.py'],
        url='https://github.com/DrSkippy/Gnacs',
        download_url='https://github.com/DrSkippy/Gnacs/tags/%s'%(GNACS_VERSION_NUMBER),
        license='LICENSE.txt',
        description='Gnip normalized activity JSON to csv parser (Twitter, Disqus Comments, and Wordpress Posts and Comments)',
        install_requires=[
                    "ujson >= 1.2",
                        ]
        )
