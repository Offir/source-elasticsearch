from distutils.core import setup

setup(
    name="panoply_elasticsearch",
    version="1.0.6",
    description="Panoply Data Source for Elasticsearch",
    author="Lior Rozen",
    author_email="lior@panoply.io",
    url="http://panoply.io",
    install_requires=[
        "panoply-python-sdk==1.3.2",
        "elasticsearch2",
        "elasticsearch5",
        "elasticsearch>=6.0.0,<7.0.0",
        "certifi==2017.4.17"
    ],

    # place this package within the panoply package namespace
    package_dir={"panoply": ""},
    packages=["panoply.es"]
)
