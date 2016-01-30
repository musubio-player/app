import endpoints

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

api_root = endpoints.api(
  name='musubio',
  version='v1',
  description='Musubio API',
  allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID],
  audiences=[ANDROID_AUDIENCE])