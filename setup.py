from distutils.core import setup

setup(
    name="panoply_elasticsearch",
    version="1.0.1",
    description="Panoply Data Source for Elasticsearch",
    author="Lior Rozen",
    author_email="lior@panoply.io",
    url="http://panoply.io",
    install_requires=[
        "panoply-python-sdk==1.3.2",
        "elasticsearch>=1.0.0,<2.0.0",
    ],

    # place this package within the panoply package namespace
    package_dir={"panoply": ""},
    packages=["panoply.es"]
)
