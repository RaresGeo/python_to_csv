#!/usr/bin/env python3
import io
import json
import csv
import argparse
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


def main(fields):
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    # File ID of the Google Drive file
    file_id = '1zLdEcpzCp357s3Rse112Lch9EMUWzMLE'

    # Fetch and download the file
    request = service.files().get_media(fileId=file_id)
    downloaded = io.BytesIO()
    downloader = MediaIoBaseDownload(downloaded, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    # Read CSV and filter the fields
    downloaded.seek(0)
    csvreader = csv.DictReader(io.StringIO(downloaded.read().decode('utf-8')))
    headers = csvreader.fieldnames

    if fields:  # Check if specific fields are requested
        for field in fields:
            if field not in headers:
                raise Exception(f"Field '{field}' not found in CSV headers.")

    json_output = {"data": []}
    for row in csvreader:
        if fields:
            json_output["data"].append({field: row[field] for field in fields})
        else:
            json_output["data"].append(row)

    # Write JSON to file
    with open('output.json', 'w') as outfile:
        json.dump(json_output, outfile, indent=4)

    print("Done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and filter a CSV from Google Drive.')
    parser.add_argument('--fields', type=str, help='Comma separated fields to filter from the CSV.')
    args = parser.parse_args()

    fields = args.fields.split(",") if args.fields else None

    main(fields)
