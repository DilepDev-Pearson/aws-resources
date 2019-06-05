import boto3 as boto3
import argparse as argparse
import time as time
from pprint import pprint

# AWS resources
import aws_resources as aws_resources

### START of ResourceHandler class
class ResourceHandler:

    def __init__(self, environment, environmentType, region, dry_run=None, request_delay=5):
        self.environment = environment;
        self.environmentType = environmentType;
        self.region = region;
        self.dry_run = dry_run;
        self.request_delay=request_delay;

        self.tagFilters = [{'Key': 'Environment', 'Values': [self.environment]}, {'Key': 'EnvironmentType', 'Values': [self.environmentType]}];
        self.client = boto3.client('resourcegroupstaggingapi', region_name = self.region);
        self.set_resources();

    def set_resources(self):
        resource_list = aws_resources.ResourceManipulator();
        resource_list.add_resources(aws_resources.acm(self.region));
        resource_list.add_resources(aws_resources.elbv2(self.region));
        
        self.resource_list = resource_list;

    def delete_resource_in_page(self, response, responseLength):
        
        if self.dry_run is not None:
            print('### DRY RUN =>');
        
        for i in range(responseLength):
            arn = response[i][u'ResourceARN']
            
            if self.dry_run is not None:
                print(arn);
            else:
                aws_resources.ResourceManipulator();
                self.resource_list.delete(arn);
                time.sleep(self.request_delay);

    def delete_resources_recursively(self, paginationToken = ''):

        responsePage = self.client.get_resources(PaginationToken=paginationToken, TagFilters = self.tagFilters);

        # paginationtoken is to cycle through next page of resources
        paginationToken = responsePage[u'PaginationToken'];

        response = responsePage[u'ResourceTagMappingList']
        responseLength = len(response);

        if paginationToken != '':
            
            self.delete_resource_in_page(response, responseLength);
            self.delete_resources_recursively(paginationToken = paginationToken);

        else:
            self.delete_resource_in_page(response, responseLength);
            print('### Done ###');

### END of ResourceHandler class

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Delete a bitesize environment")
    parser.add_argument('--env', required=True);
    parser.add_argument('--region', required=True);
    parser.add_argument('--envtype', required=True);
    
    parser.add_argument('--dry-run', action='count');
    parser.add_argument('--delete', action='count');
    parser.add_argument('--request-delay', type=int, choices=xrange(1, 120), default=5);
    args = parser.parse_args()

    env = args.env;
    region = args.region;
    envtype = args.envtype;
    dry_run = args.dry_run;
    delete = args.delete
    request_delay = args.request_delay;

    resourceHandler = ResourceHandler(env, envtype, region, dry_run=dry_run, request_delay=request_delay);
    
    if delete is 1:    
        resourceHandler.delete_resources_recursively();