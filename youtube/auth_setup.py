import os
import pickle
import argparse

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate_and_save_token(token_path, client_secrets_file):
    creds = None

    # Check if token already exists
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token_file:
            creds = pickle.load(token_file)

    # Refresh or generate new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(token_path, 'wb') as token_file:
            pickle.dump(creds, token_file)

    print("✅ Token saved successfully to", token_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Authenticate with YouTube API and save token.")
    parser.add_argument('--token', type=str, required=True, help='Path to the token.pickle file')
    parser.add_argument('--secrets', type=str, required=True, help='Path to the client_secrets.json file')
    args = parser.parse_args()

    authenticate_and_save_token(args.token, args.secrets)
