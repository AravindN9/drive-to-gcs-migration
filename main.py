import os
import io
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.cloud import storage


def move_drive_to_gcs():
    # Fetch variables set during deployment
    DRIVE_FILE_ID = os.environ.get("DRIVE_FILE_ID")
    GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
    DESTINATION_BLOB_NAME = os.environ.get("DESTINATION_BLOB_NAME", "migrated_data.csv")

    print(f"Starting migration for file ID: {DRIVE_FILE_ID}")

    # Authenticate automatically using the Service Account attached to Cloud Run
    credentials, project = google.auth.default()

    # Initialize the Drive API client
    drive_service = build('drive', 'v3', credentials=credentials)
    request = drive_service.files().get_media(fileId=DRIVE_FILE_ID)

    # Download the file into computer memory (RAM) instead of saving to a hard drive
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    file_stream.seek(0)  # Reset the stream's cursor back to the beginning to read it for upload

    # Initialize the Cloud Storage client
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(DESTINATION_BLOB_NAME)

    # Upload from memory to the bucket
    blob.upload_from_file(file_stream, content_type='text/csv')
    print(f"Success! File moved to gs://{GCS_BUCKET_NAME}/{DESTINATION_BLOB_NAME}")


if __name__ == "__main__":
    move_drive_to_gcs()
