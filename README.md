# zendesk-ticket-viewer

 
# Run by executing the below commands

1. Ensure you have enabled username/password authentication on your Zendesk developer settings.
2. Install package dependencies using `pip install -r ./requirements.txt`
3. Set your Zendesk credentials using environment variables:
    export ZENDESK_USERNAME=<username>
    export ZENDESK_PASSWORD=<password>
4. Run the application using `python zendesk_viewer/app.py`

# Testing

1. Install test dependencies using `pip install -r ./requirements_test.txt`
2. Run `pytest` to run all tests

# Coverage

1. Run `pytest --cov-report html --cov='.'`
2. View html report generated in ./html dir

# License

This project is licensed under the MIT license. See the LICENSE file for details.