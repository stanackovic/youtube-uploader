import os
import pickle
import argparse

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Constants
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service(token_path):
    if not os.path.exists(token_path):
        raise Exception(f"❌ token.pickle not found at {token_path}. Run auth_setup.py first to authenticate.")

    with open(token_path, 'rb') as token_file:
        creds = pickle.load(token_file)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build('youtube', 'v3', credentials=creds)

def upload_video(
    file_path,
    title,
    description,
    tags,
    category_id,
    privacy_status,
    made_for_kids,
    token_path
):
    youtube = get_authenticated_service(token_path)

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id,
        },
        'status': {
            'privacyStatus': privacy_status,
            'madeForKids': made_for_kids,
            'selfDeclaredMadeForKids': made_for_kids
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/*')

    print("🚀 Uploading video...")
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"⏳ Uploaded {int(status.progress() * 100)}%")

    print("✅ Upload complete! Video ID:", response['id'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a video to YouTube")
    parser.add_argument('--file', required=True, help='Path to video file')
    parser.add_argument('--title', required=True, help='Video title')
    parser.add_argument('--description', default='', help='Video description')
    parser.add_argument('--tags', default='', help='Comma-separated list of tags')
    parser.add_argument('--privacy', default='public', choices=['public', 'private', 'unlisted'], help='Privacy status')
    parser.add_argument('--category', default='22', help='YouTube category ID (default is 22 - People & Blogs)')
    parser.add_argument('--kids', action='store_true', help='Mark as made for kids')
    parser.add_argument('--token', required=True, help='Path to token.pickle file')

    args = parser.parse_args()
    tags_list = [tag.strip() for tag in args.tags.split(',')] if args.tags else []

    upload_video(
        file_path=args.file,
        title=args.title,
        description=args.description,
        tags=tags_list,
        category_id=args.category,
        privacy_status=args.privacy,
        made_for_kids=args.kids,
        token_path=args.token
    )
