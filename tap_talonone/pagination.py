from urllib.parse import parse_qs, urlparse

from singer_sdk.pagination import BaseOffsetPaginator


class Paginator(BaseOffsetPaginator):

    def has_more(self, response):
        data = response.json()
        if data.get('hasMore') != None:
            return data['hasMore']
        parsed_url = urlparse(response.request.url)
        current_skip = parse_qs(parsed_url.query)['skip'][0]
        if data.get('data'):
            return int(current_skip) + len(data['data']) < data['totalResultSize']
        return False
