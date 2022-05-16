
'''
Write a script that creates a public S3 website bucket. 
Must have the following: 1.index file 2.error file 3.return the status code of a curl test.
'''
import boto3
import os
import json
import requests

s3 = boto3.client('s3')
s3Resource = boto3.resource('s3')


def main():
    bucket = "jayaganeshtestwebsitebuckettest123"

    existingBukcet = BucketExists(bucket)
    if existingBukcet == False:
        createBucket(bucket)

    uploadFiles(bucket, "web")

    makeObjectsPublic(bucket)

    enableStaticWebsite(bucket)

    websiteStatus(bucket)


def BucketExists(bucket):
    try:
        s3.head_bucket(Bucket=bucket)
        return True
    except Exception as e:
        return False


def createBucket(bucket):
    print("Creating Bucket...")
    try:
        createBucketResponse = s3.create_bucket(
            Bucket=bucket)
        if createBucketResponse['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Bucket Created Successfully.")
            return True
        else:
            print("Bucket Creation Failed.")
            return False
    except Exception as e:
        print("Bucket Creation Failed.")
        return False


def uploadFiles(bucket, directory):
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
                s3.upload_file(
                    filePath, bucket, fileName, ExtraArgs={
                        'ContentType': 'text/html'})
                # data = open(filePath)
                # s3.put_object(
                #     Body=data,
                #     Bucket=bucket,
                #     ContentType='text/html',
                #     Key=fileName
                # )
                print("Uploaded: ", filePath)
            except Exception as e:
                print("File Upload Failed." + str(e))
            print("\n")


def makeObjectsPublic(bucket):
    try:
        Policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Principal': '*',
                    'Action': ['s3:GetObject'],
                    'Resource': 'arn:aws:s3:::'+bucket+'/*'
                }
            ]
        }

        bucketPolicy = s3.put_bucket_policy(
            Bucket=bucket,
            Policy=json.dumps(Policy),
        )
        # print(bucketPolicy)

    except Exception as e:
        print("Bucket Policy Creation Failed. " + str(e))
        return False


def enableStaticWebsite(bucket):
    try:
        staticWebsite = s3.put_bucket_website(
            Bucket=bucket,
            WebsiteConfiguration={
                'ErrorDocument': {
                    'Key': 'error.html'
                },
                'IndexDocument': {
                    'Suffix': 'index.html'
                }
            },
        )
        # print(staticWebsite)
        if staticWebsite['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Static Website Enabled Successfully.")
            return True
        else:
            print("Static Website Creation Failed.")
            return False
    except Exception as e:
        print("Static Website Creation Failed.")
        return False


def websiteStatus(bucket):
    try:
        r = requests.get(
            'http://'+bucket+'.s3-website-us-east-1.amazonaws.com')
        if r.status_code == 200:
            print("Website Status Code: " + str(r.status_code))
        else:
            print("Website is not Live.")
    except Exception as e:
        print("Website is not Live.")


if __name__ == "__main__":
    main()
