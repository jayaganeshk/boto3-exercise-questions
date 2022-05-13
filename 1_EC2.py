import time
import boto3
ec2 = boto3.client('ec2')
ec2Resource = boto3.resource('ec2')


def main():
    instanceNames = [
        "web1",
        "web2",
        "web3",
    ]

    amiID = "ami-0022f774911c1d690"
    keyPairName = 'test'
    subnetID = "subnet-0caf3a64479da1cba"
    securityGroupID = "sg-0f386be704283d1fa"

    instanceIDs = []

    isKeyPairExists = keyPairExists(keyPairName)
    if isKeyPairExists == False:
        createKeyPair(keyPairName)

    for instanceName in instanceNames:
        instanceID = createInstance(
            instanceName,
            amiID, keyPairName,
            subnetID, securityGroupID
        )
        if instanceID != False:
            print("created instance: " + instanceName +
                  " and its ID is: " + instanceID)
            instanceIDs.append(instanceID)

    print("Waiting for instances to be in ready state...")
    instanceDetails = describeInstances(instanceIDs)
    print("\n")
    if instanceDetails != False:
        for instanceDetail in instanceDetails:
            print(" Instance Name: " + instanceDetail['instanceName'] + " Instance ID: " + instanceDetail['instanceID'] +
                  " Public IP: " + instanceDetail['publicIP']
                  )
    else:
        print("Error getting instance IPs")


def createKeyPair(keyName):
    print("Creating Key Pair: " + keyName)
    try:
        createKeyPairResponse = ec2.create_key_pair(
            KeyName=keyName
        )
        print(createKeyPairResponse)
        with open(keyName + ".pem", "w") as f:
            f.write(createKeyPairResponse["KeyMaterial"])
    except Exception as e:
        print(e)


def keyPairExists(keyName):
    try:
        keyPairExistsResponse = ec2.describe_key_pairs(
            KeyNames=[
                keyName
            ],
        )
        # print(keyPairExistsResponse)
        print("Key Pair Exists: " + keyName)
        return True
    except Exception as e:
        print('Key Pair does not exist')
        return False


def createInstance(instanceName, amiID, keyName, subnetID, securityGroupID):
    print("Creating Instance: " + instanceName)
    try:
        createInstanceResponse = ec2Resource.create_instances(
            ImageId=amiID,
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            # SubnetId=subnetID,
            # SecurityGroupIds=[
            #     securityGroupID,
            # ],
            KeyName=keyName,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instanceName
                        },
                    ]
                },
            ],
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 8,
                        'VolumeType': 'standard'
                    },
                },
            ],
            NetworkInterfaces=[{
                "DeviceIndex": 0,
                "SubnetId": subnetID,
                "AssociatePublicIpAddress": True,
                "Groups": [
                    securityGroupID,
                ]
            }]
            # DryRun=True,
        )
        instanceID = createInstanceResponse[0].id
        return instanceID
    except Exception as e:
        print("Error creating instance: " + instanceName + " " + str(e))
        return False


def describeInstances(instanceIDs):
    try:
        time.sleep(30)
        describeInstancesResponse = ec2.describe_instances(
            InstanceIds=instanceIDs,
        )
        Reservations = describeInstancesResponse['Reservations']
        InstanceDetails = []
        for reservation in Reservations:
            instances = reservation['Instances']
            for instance in instances:
                try:
                    publicIP = instance['PublicIpAddress']

                    Tags = instance['Tags']
                    InstanceName = ""
                    for tag in Tags:
                        if tag['Key'] == 'Name':
                            InstanceName = tag['Value']

                    InstanceDetails.append({
                        'instanceID': instance['InstanceId'],
                        'publicIP': publicIP,
                        'instanceName': InstanceName
                    })

                except Exception as e:
                    print("Public IP not allocated yet..Retying in 30 seconds")
                    time.sleep(30)
                    describeInstances(instanceIDs)
        return InstanceDetails
    except Exception as e:
        print("Error describing instances: " + str(e))
        return False


if __name__ == "__main__":
    main()
