# Questions

1. Write a script that builds three 512 MB EC2 Instances that following a similar naming convention.
   (ie., web1, web2, web3) and returns the IP of each instance. Use any image you want.

2. Write a script that accepts a directory as an argument as well as a S3 bucket name. The script should upload the contents of the specified directory to the S3 Bucket (or create it if it doesn't exist). The script should handle errors appropriately. (Check for invalid paths, etc.)
3. Write a script that creates a public S3 website bucket. Must have the following:
   1.index file
   2.error file
   3.return the status code of a curl test.
4. Write an application that will create a SQS queue and send it a message.
5. Write an application that prints hello world if the SQS queue has a message
