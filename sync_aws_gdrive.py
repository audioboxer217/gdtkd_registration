import io
import os
import boto3
from dotenv import load_dotenv
import backend.process_entries as pe

load_dotenv("backend.env")


def main():
    bucket = os.environ.get("BADGE_BUCKET")

    s3 = boto3.client("s3")
    badges = s3.list_objects(Bucket=bucket)["Contents"]

    for badge in badges:
        file_name = badge["Key"]
        print(f"Syncing {file_name}")

        file_obj = io.BytesIO()
        s3.download_fileobj(Bucket=bucket, Key=file_name, Fileobj=file_obj)
        file_obj.seek(0)

        # Upload to GDrive
        gdrive_creds_file = s3.get_object(
            Bucket=os.getenv("CONFIG_BUCKET"),
            Key="tkd-reg_service_account.json",
        )["Body"].read()
        pe.upload_to_gdrive(
            file_obj,
            os.getenv("BADGE_GFOLDER"),
            file_name,
            gdrive_creds_file,
        )
        print("  done")


if __name__ == "__main__":
    main()
