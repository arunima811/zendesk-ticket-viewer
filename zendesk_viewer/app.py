from api import ZendeskApiClient
from ui import console

client = ZendeskApiClient.ZendeskApiClient()

if __name__ == '__main__':
    user_name = client.get_user()
    if user_name:
        console.draw_home_ui(client, user_name)
    else:
        console.show_error("ERROR", "Unbale to connect to Zendesk API", "Ensure ZENDESK_USERNAME and ZENDESK_PASSWORD environment varibales are set correctly")