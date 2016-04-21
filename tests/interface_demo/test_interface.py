import unittest

import datetime

from interface_demo.interface import CachablePnLExplainer


class testInterface(unittest.TestCase):

    def testMakeAnInterface(self):
        data_fetch_function = lambda *args, **kwargs:None
        i = CachablePnLExplainer(data_fetch_function=data_fetch_function, cache={})


    def test_actual_caching_happens(self):
        def fake_data_fetch_function(date, books):
            return {
                date:{b:{} for b in books}
            }
        cache = {}
        i = CachablePnLExplainer(data_fetch_function=fake_data_fetch_function, cache=cache)
        date = datetime.date(2015,1,1)
        books = ["ABCD", "DEFG", "HIJK"]
        i.get_result_for_one_day(date, books)
        self.assertEqual(cache[date]["ABCD"], {})


    def test_cache_does_not_request_anything_if_already_cached(self):
        cob_date = datetime.date(2015,1,1)
        books = ["ABCD", "DEFG", "HIJK"]

        cache = {
            cob_date:{b:{} for b in books}
        }

        def fake_data_fetch_function(*args, **kwargs):
            raise RuntimeError("This function should not have been called.")

        i = CachablePnLExplainer(data_fetch_function=fake_data_fetch_function, cache=cache)
        result = i.get_result_for_one_day(cob_date, ["DEFG"])
        self.assertIs(result[cob_date]["DEFG"], cache[cob_date]["DEFG"])




if __name__ == "__main__":
    unittest.main()