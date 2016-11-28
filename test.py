import unittest
from mock import call, patch, Mock
from es import ElasticsearchSource, IDPATTERN, DESTINATION

OPTIONS = {
    "logger": lambda *msgs: None, # no-op logger
}


class TestElasticsearch(unittest.TestCase):

    source = None

    def setUp(self):
        self.source = {
            "host": "h:p",
            "indices": ["bank", "customers"]
        }

    def tearDown(self):
        self.source = None

    def test_defaults(self):
        ElasticsearchSource(self.source, OPTIONS)
        self.assertEqual(self.source["idpattern"], IDPATTERN)
        self.assertEqual(self.source["destination"], DESTINATION)

    # fetches list of indices from host
    @patch("elasticsearch.client.CatClient.indices")
    def test_get_indices(self, mock_indices_func):
        mock_indices = [
            { "index": "tweets", "docs.count": 1 },
            { "index": "stories", "docs.count": 2 },
            { "index": "photos", "docs.count": 3 }
        ]
        mock_indices_func.return_value = mock_indices

        indices = ElasticsearchSource(self.source, OPTIONS).get_indices()
        mock = mock_indices[0]
        index = indices[0]

        self.assertEqual(len(indices), len(mock_indices))
        self.assertEqual(index.get("count"), mock.get("docs.count"))
        self.assertEqual(index.get("title"), mock.get("index"))

    # ensure that, when passed inc_key & val, they appear in the query
    @patch("elasticsearch.Elasticsearch.search")
    def test_uses_inc_key(self, mock_search):
        self.source["incKey"] = "age"
        self.source["incVal"] = 40
        stream = ElasticsearchSource(self.source, OPTIONS)

        stream.read()
        kwargs = mock_search.call_args[1]
        inc_filter = kwargs["body"]["query"]["bool"]["filter"]["range"]

        self.assertTrue( self.source["incKey"] in inc_filter )

    # ensure that all indices are returned
    @patch("elasticsearch.Elasticsearch.clear_scroll")
    def test_get_data(self, mock_clear_scroll):
        res = { "_scroll_id": "fake_scroll", "total": 0 }
        stream = ElasticsearchSource(self.source, OPTIONS)
        stream._search = Mock(return_value = res)

        stream.read()

        arg_list = stream._search.call_args_list
        # Called for both indices
        self.assertEquals( stream._search.call_count, 2 )
        # Called for each index
        self.assertEquals( arg_list, [call("customers"), call("bank")] )

    # ensure that once all docs are fetched for an index,
    # the scroll_id is deleted and index counters are reset
    @patch("elasticsearch.Elasticsearch.clear_scroll")
    def test_reset_after_index(self, mock_clear_scroll):
        res = { "_scroll_id": "fake_scroll", "total": 0 }
        stream = ElasticsearchSource(self.source, OPTIONS)
        stream._search = Mock(return_value = res)

        stream.read()

        # Called for each index
        self.assertEquals( mock_clear_scroll.call_count, 2 )

    # ensure that while an index is being processed, calling
    #  _get_index will return the same index
    def test_get_index(self):
        stream = ElasticsearchSource(self.source, OPTIONS)

        first_call = stream._get_index()
        stream.index = first_call
        second_call = stream._get_index()

        stream._reset_index()
        third_call = stream._get_index()

        # With an index set, the second call should be the same
        success = first_call == second_call == self.source["indices"][-1]
        self.assertTrue(success)

        self.assertEqual(third_call, self.source["indices"][0])


# Run the test suite
if __name__ == "__main__":
    unittest.main()
