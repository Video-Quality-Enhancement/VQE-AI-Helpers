import dotenv
import os
import datetime
from google.cloud import storage
from google.oauth2.service_account import Credentials

class GoogleCloudStorage:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        credentials = Credentials.from_service_account_file("credentials.json")
        self.storage_client = storage.Client(credentials=credentials, project=os.getenv("PROJECT_ID"))
        self.bucket = self.storage_client.get_bucket(os.getenv("BUCKET_NAME"))

    def upload(self, filepath: str, emailid: str):
        myfile_blob = self.bucket.blob(filepath)
        myfile_blob.upload_from_filename(filepath)

        print(f"File {filepath} uploaded to {os.getenv('BUCKET_NAME')}")

        # Granting access to the file to the emailid
        myfile_blob.acl.user(emailid).grant_read()

        # get signed url for the emailid
        expiration_time = datetime.timedelta(hours=1)
        url = myfile_blob.generate_signed_url(expiration_time, method="GET")

        return f"https://storage.googleapis.com/{os.getenv('BUCKET_NAME')}/{filepath}"
    
    def list_files(self):
        blobs = self.bucket.list_blobs()
        for blob in blobs:
            print(blob.name)


def main():
    emailid = "ankit2001das@gamil.com"
    filepath = "Wildlife.mp4"

    cloud_storage = GoogleCloudStorage()

    url = cloud_storage.upload(filepath, emailid)
    print(f"File uploaded: {url}")

if __name__ == "__main__":
    main()
