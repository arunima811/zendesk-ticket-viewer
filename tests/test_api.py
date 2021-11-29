from unittest import mock

from zendesk_viewer.api import ZendeskApiClient

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    base_url = "https://zccintern22.zendesk.com/api/v2/tickets.json?page[size]=25"
    if args[0] == base_url:
        return MockResponse({"tickets": [], "links": {"next": "next", "prev": "prev"}, "meta": {"has_more": True}}, 200)
    elif args[0] == 'next':
        return MockResponse({"tickets": [],"links": {"next": None, "prev": base_url}, "meta": {"has_more": False}}, 200)
    elif args[0] == 'prev':
        return MockResponse({"tickets": [],"links": {"next": base_url, "prev": None}, "meta": {"has_more": True}}, 200)
    elif args[0] == 'https://zccintern22.zendesk.com/api/v2/users/me':
        return MockResponse({"user": {"id": 1, "name": "John Doe"}}, 200)

    return MockResponse(None, 404)

@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_user_name(mock_get):
    client = ZendeskApiClient.ZendeskApiClient()
    assert client.get_user() == "John Doe"

@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_next(mock_get):
    client = ZendeskApiClient.ZendeskApiClient()
    assert client.has_next() == True
    assert client.has_prev() == False
    assert client.get_tickets('next') is not None
    assert client.has_next() == True
    assert client.has_prev() == True

@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_prev(mock_get):
    client = ZendeskApiClient.ZendeskApiClient()
    assert client.has_next() == True
    assert client.has_prev() == False
    assert client.get_tickets('next') is not None
    assert client.get_tickets('prev') is not None
    assert client.has_next() == True
    assert client.has_prev() == False

@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_reset(mock_get):
    client = ZendeskApiClient.ZendeskApiClient()
    assert client.get_tickets('next') is not None
    assert client.get_tickets('next') is not None
    client.reset()
    assert client.get_tickets('next') is not None