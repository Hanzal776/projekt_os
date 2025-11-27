# Flask Audio Transcription (scaffold)

Small Flask app for uploading audio files and forwarding them to a transcription API.

## Usage

### 1. Environment Setup
Copy `.env.example` to `.env` and edit the values as needed:

```bash
cp .env.example .env
```

### 2. Build and Run with Docker

#### Build the Docker Image
```bash
docker build -t audio-transcribe .
```

#### Run the Container
```bash
docker run -p 5000:5000 --env-file .env -v $(pwd)/uploads:/app/uploads audio-transcribe
```

### 3. Use Docker Compose

#### Build and Start Services
```bash
docker compose up --build
```

#### Stop Services
```bash
docker compose down
```

### 4. Access the Application
Open your browser and navigate to:
- [http://localhost:5000](http://localhost:5000)

## Endpoints
- `/` - Upload form
- `/transcribe` - POST upload and forward to API

## Environment Variables
Documented in `.env.example`.

## Kubernetes Deployment
Refer to `k8s/` directory for deployment and service manifests.
