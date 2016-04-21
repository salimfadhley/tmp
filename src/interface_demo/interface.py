import collections

def recursive_update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = recursive_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

class CachablePnLExplainer(object):

    def __init__(self, data_fetch_function, cache):
        self.data_loading_function = data_fetch_function
        self.cache = cache

    def purge(self, maximum_age=40):
        """
        Purge any record older than maximum age
        """

    def update_cache(self, data):
        recursive_update(self.cache, data)
        return data

    def fetch_from_cache(self, cob_date, books):
        return {
            cob_date:{b:self.cache[cob_date][b] for b in books}
        }

    def get_result_for_one_day(self, cob_date, books):

        if cob_date in self.cache:
            if set(books).issubset(self.cache[cob_date]):
                return self.fetch_from_cache(cob_date, books)

        self.update_cache(self.data_loading_function(cob_date, books))
        return self.fetch_from_cache(cob_date, books)
