'''
Write a script that accepts a directory as an argument as well as a S3 bucket name. 
The script should upload the contents of the specified directory to the S3 Bucket (or create it if it doesn't exist). 
The script should handle errors appropriately. (Check for invalid paths, etc.)

python .\2_S3Upload.py .\test jayaganeshtes00
'''

import boto3
import os
import sys

s3 = boto3.client('s3')


def main():
    if len(sys.argv) == 1:
        directory = input("Enter Directory Path: ")
        bucket = input("Enter Bucket Name: ")
    else:
        directory = sys.argv[1]
        bucket = sys.argv[2]

    print("Directory: ", directory)
    print("Bucket: ", bucket)
    print("\n")
    isValidDir = os.path.isdir(directory)

    if isValidDir != True:
        print("Invalid Directory.")
        return False

    existingBukcet = BucketExists(bucket)

    if existingBukcet == False:
        createBucket(bucket)

    uploadFile(bucket, directory)


def BucketExists(bucket):
    try:
        s3.head_bucket(Bucket=bucket)
        return True
    except Exception as e:
        return False


def createBucket(bucket):
    print("Creating Bucket...")
    try:
        createBucketResponse = s3.create_bucket(Bucket=bucket)
        if createBucketResponse['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Bucket Created Successfully.")
            return True
        else:
            print("Bucket Creation Failed.")
            return False
    except Exception as e:
        print("Bucket Creation Failed.")
        return False


def uploadFile(bucket, directory):
    print("Uploading Files...")
    len0 = len(directory)
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            len1 = len(os.path.join(root, file))
            sub = len0 - len1
            filePath = os.path.join(root, file)
            fileName = filePath[len0 + 1:].replace("\\", "/")
            print("Uploading File: " + file)
            filePath = os.path.join(root, file)
            try:
                s3.upload_file(filePath, bucket, fileName)
                print("Uploaded: ", filePath)
            except Exception as e:
                print("File Upload Failed.")
            print("\n")


if __name__ == "__main__":
    main()
