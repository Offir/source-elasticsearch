from es import *
import sys

source = {
    "host": "127.0.0.1:9200",
    "indices": [ { "value": "bank" } ]
}

stream = es.ElasticsearchSource(source,{})
while True:
    data = stream.read()
    print "Got data!", len(data)
    if not data:
        sys.exit()

