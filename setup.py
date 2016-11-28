from distutils.core import setup

setup(
    name="panoply_elasticsearch",
    version="1.0.0",
    description="Panoply Data Source for Elasticsearch",
    author="Lior Rozen",
    author_email="lior@panoply.io",
    url="http://panoply.io",
    install_requires=[
        "panoply-python-sdk"
    ],

    # place this package within the panoply package namespace
    package_dir={"panoply": ""},
    packages=["panoply.es"]
)
