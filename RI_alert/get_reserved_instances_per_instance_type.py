import boto3

def get_reservedInstances(region_name):
    ec2 = boto3.client('ec2', region_name=region_name)
    Reserved_instances = ec2.describe_reserved_instances()
    instances = Reserved_instances.get('ReservedInstances')
    result = {}
    for i in instances:
        if(i.get('State')=='active'):
            if(result.get(i.get('InstanceType'))):
                count = result.get(i.get('InstanceType'))+i.get('InstanceCount')
                result[i.get('InstanceType')] = count
            else:
                result[i.get('InstanceType')] = i.get('InstanceCount')
    return(result)
