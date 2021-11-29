import os

def pytest_generate_tests(metafunc):
    os.environ["ZENDESK_USERNAME"] = "user"
    os.environ["ZENDESK_PASSWORD"] = "pass"