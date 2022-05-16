'''
Write an application that will create a SQS queue 
and send it a message.
'''

import boto3
import datetime
sqs = boto3.client('sqs')


def main():
    queueName = "jayaganeshtestqueue1.fifo"
    queueURL = getQueueURL(queueName)
    if queueURL == False:
        queueURL = createQueue(queueName)
    print("queueURL: ", queueURL)

    message = 'Test Message from JayaGanesh at ' + str(datetime.datetime.now())
    sendMessage(queueURL, message)


def getQueueURL(queueName):
    try:
        queueExistsresponse = sqs.get_queue_url(
            QueueName=queueName
        )
        return queueExistsresponse['QueueUrl']
    except Exception as e:
        print("Queue Does Not Exist.")
        return False


def createQueue(queueName):
    try:
        createQueueresponse = sqs.create_queue(
            QueueName=queueName,
            Attributes={
                'FifoQueue': 'true',
                'ContentBasedDeduplication': 'true'
            }
        )
        if createQueueresponse['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Queue Created Successfully.")
            return createQueueresponse['QueueUrl']
        else:
            print("Queue Creation Failed.")
            return False
    except Exception as e:
        print("Queue Creation Failed.", e)
        return False


def sendMessage(queueURL, message):
    try:
        response = sqs.send_message(
            QueueUrl=queueURL,
            MessageBody=(
                message
            ),
            MessageGroupId=str(datetime.datetime.now().timestamp()),
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Message Sent Successfully.")
        else:
            print("Message Sending Failed.")
    except Exception as e:
        print("Message Sending Failed.", e)


if __name__ == "__main__":
    main()
