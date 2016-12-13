import httplib
import urllib
import json
import base64

class HTTPLibWrapper():

    host = None
    version = None
    def __init__(self, _host = None):
        if not _host:
            raise HTTPLibError("Host and port are required")

        self.host = _host

        # Verify that we can make a connection
        resp = self._request( "GET", "")
        version = resp["version"]["number"]
        self.version = int(version.split(".")[0])
        print "Elasticsearch version: %s. Cluster: %s" % (
            resp["version"]["number"], resp["cluster_name"]
        )

    # Returns a list of indices containing only the
    # specified fields in a json format
    def get_indices(self):
        fields = ["index", "docs.count"]
        params = { "h": ",".join(fields) }
        url = "/_cat/indices?format=json"
        res = self._request("GET", url, params)
        return res

    def search(self, index, params, scroll):
        if params["_source_excludes"] is None:
            del params["_source_excludes"]

        url = "/%s/_search?scroll=%s" % ( index, scroll )
        data = self._request("POST", url, params)
        return data

    '''
        0.90 - scroll & scroll_id in URL params
        1.3 - scroll in URL, scroll_id as request BODY
        2.0 - scroll & scroll_id as JSON in request BODY
    '''
    def scroll(self, scroll_id, durration):

        url = "/_search/scroll"
        params = {}

        if self.version < 1: # compatibility with 0.9
            url += "?scroll=%s&scroll_id=%s" % (durration, scroll_id)
        elif self.version < 2: # compatibility with 1.3-7
            url += "?scroll=%s" % durration
            params = scroll_id
        else: # compatibility with >= 2.0
            params = {"scroll": durration, "scroll_id": scroll_id}

        data = self._request("POST", url, params )
        return data

    def clear_scroll(self, scroll_id):


    # Performs the actual HTTP request
    def _request(self, method, url, params = {}):

        # With older versions of the elasticsearch API,
        # there are parameter that are required to be plain strings
        # in the body of a request. Only convert to a json object
        # if the params that were passed are of type 'dict'
        if type(params) is dict:
            params = json.dumps(params)

        conn = httplib.HTTPConnection(self.host)

        print "REQUEST: %s %s %s" % (method, url, params)
        conn.request(method, url, params)
        resp = conn.getresponse()
        # if resp.status is not 200:
        #     raise HTTPLibError(resp.reason)

        data = resp.read()
        print "RESPOJSE RAW: ", data[:600]
        json_res = json.loads(data)
        return json_res


class HTTPLibError(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message
