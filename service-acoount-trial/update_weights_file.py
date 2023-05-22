from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

def get_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service


def print_mime_type():
    file_id="1OxH4i9cjqPedpy-khyJzBhEFb8Pqhv2Q"
    drive = get_drive_service()
    request = drive.files().get(fileId=file_id, fields='mimeType').execute()
    print(request)


def update_weights_file():
    file_id="1OxH4i9cjqPedpy-khyJzBhEFb8Pqhv2Q"  # ! trailing comma can cause problems in python and google drive api
    local_file_path="vfi-last_step_weights.pt"

    drive = get_drive_service()
    media = MediaFileUpload(local_file_path,
                            mimetype='application/x-zip',
                            resumable=True)
    
    print("Starting to upated the weights file...")
    
    file = drive.files().update(fileId=file_id,
                                body={},
                                media_body=media,
                                fields='id').execute()
    
    print(f'Updated File With ID: {file.get("id")}')
    

def main():
    print_mime_type()
    update_weights_file()

if __name__ == '__main__':
    main()