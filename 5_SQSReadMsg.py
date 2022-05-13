'''
Write an application that prints hello world if the SQS queue has a message
'''

import boto3
sqs = boto3.client('sqs')

receiptHandles = []


def main():
    queueName = "jayaganeshtestqueue0.fifo"
    queueURL = getQueueURL(queueName)
    if queueURL:
        readMessage(queueURL)

    # for receiptHandle in receiptHandles:
    #     deleteMessage(queueURL, receiptHandle)


def getQueueURL(queueName):
    try:
        queueExistsresponse = sqs.get_queue_url(
            QueueName=queueName
        )
        return queueExistsresponse['QueueUrl']
    except Exception as e:
        print("Queue Does Not Exist.")
        return False


def readMessage(queueURL):
    try:
        readMessageresponse = sqs.receive_message(
            QueueUrl=queueURL,
            AttributeNames=[
                'All'
            ],
        )
        messages = readMessageresponse['Messages']
        for message in messages:
            receiptHandles.append(message['ReceiptHandle'])
            print("Hello world!")
    except:
        print("There are no messages in the queue.")
        return False


def deleteMessage(queueURL, ReceiptHandle):
    try:
        deleteMessageresponse = sqs.delete_message(
            QueueUrl=queueURL,
            ReceiptHandle=ReceiptHandle
        )
        if deleteMessageresponse['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Message Deleted Successfully.")
            return True
        else:
            print("Message Deletion Failed.")
            return False
    except Exception as e:
        print("Message Deletion Failed.", e)
        return False


if __name__ == '__main__':
    main()
