from distutils.core import setup

setup(
    name="panoply_elasticsearch",
    version="1.0.2",
    description="Panoply Data Source for Elasticsearch",
    author="Lior Rozen",
    author_email="lior@panoply.io",
    url="http://panoply.io",
    install_requires=[
        "panoply-python-sdk==1.3.2",
        "elasticsearch==2.4.1",
    ],

    # place this package within the panoply package namespace
    package_dir={"panoply": ""},
    packages=["panoply.es"]
)
