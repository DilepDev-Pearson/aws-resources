import boto3 as boto3


class Resource:

    def __init__(self):
        pass        


class acm(Resource):

    def __init__(self, region_name):
        self.key = 'arn:aws:acm';
        self.client = boto3.client('acm', region_name = region_name);

    def delete(self, arn):
        print('Deleting Certificate (ACM) => %s' % (arn));
        self.client.delete_certificate(CertificateArn = arn);


class elbv2(Resource):

    def __init__(self, region_name):
        self.key = 'arn:aws:elasticloadbalancing'
        self.client = boto3.client('elbv2', region_name = region_name);

    def delete(self, arn):
        print('Deleting Loadbalancer (ELBv2) => %s' % (arn));
        self.client.delete_load_balancer(LoadBalancerArn = arn);


class ResourceManipulator():

    def __init__(self):
        self.resources = [];

    def add_resources(self, resource):
        self.resources.append(resource);

    def delete(self, arn):

        for resource in self.resources:
            #if there is matching key at index 0 of ARN
            if arn.find(resource.key) == 0:
                resource.delete(arn);
                # print(arn);