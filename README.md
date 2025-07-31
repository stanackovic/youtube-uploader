# YouTube Video Uploader

Automate the upload of YouTube Videos with support for metadata like title, description, tags, category, and privacy status.

Built with:
- Python
- YouTube Data API v3
- OAuth2.0 Authentication (token-based)

---

## Features

- ✅ Uploads videos to YouTube using existing OAuth `token.pickle`
- ✅ Configure metadata: title, description, tags, category, privacy, etc.
- ✅ Built-in progress display
- ✅ One-time browser login flow for token generation
- ✅ Docker support ready
- ❌ No Service Account support (not allowed by YouTube for uploads)

---

## First-Time Setup

### 1. Create Google OAuth Credentials

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project
- Enable the **YouTube Data API v3**
- Go to **APIs & Services > Credentials**
- Create **OAuth Client ID** → Application Type: **Desktop**
- Download `client_secrets.json` and place it in the project root

### 2. Authenticate and Generate Token

Run this once in your terminal:

```bash
python youtube/auth_setup.py --token credentials/token.pickle --secrets credentials/client_secrets.json

```

It will open a browser to authorize your YouTube channel and save `token.pickle`.

---

## Upload a Video

Use the `upload.py` script:

```bash
python3 youtube/upload.py \
  --file shorts/my_video.mp4 \
  --title "Sample title #shorts" \
  --description "Description. #shorts" \
  --tags "motivation,quotes,shorts" \
  --privacy public \
  --category 22
```

### Command Line Options

| Argument        | Description                                  |
|----------------|----------------------------------------------|
| `--file`        | Path to the video file                       |
| `--title`       | Title of the video                           |
| `--description` | Description for the video                    |
| `--tags`        | Comma-separated tags                         |
| `--privacy`     | `public`, `private`, or `unlisted`           |
| `--category`    | YouTube Category ID (default: `22`)          |
| `--kids`        | Include this flag to mark "Made for Kids"    |

---

## 🐳 Run via Docker

### 1. Build Docker image

```bash
docker build -t youtube-uploader docker/Dockerfile
```

### 2. Run Upload Script

```bash
docker run -it --rm \
    -v "$PWD/secrets:/app/secrets" \
    -v "$PWD/videos:/app/videos" \
    -v "$PWD:/app" \
    youtube-uploader \
    python youtube/uploader.py \
        --file videos/myvideo.mp4 \
        --title "My Title" \
        --description "Description here" \
        --tags "tag1,tag2" \
        --privacy public \
        --token secrets/token.pickle

```

> ⚠️ Make sure you’ve already authenticated with `token.pickle` outside Docker, or run `auth_setup.py` interactively with port access.

---

## Security Notes

- Your `token.pickle` holds OAuth tokens; treat it like a password.
- Store `client_secrets.json` and `token.pickle` securely.
- You can encrypt and decrypt the token in CI/CD if needed.
