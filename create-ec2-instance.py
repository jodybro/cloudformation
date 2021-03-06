#!/usr/bin/env python3.7
# Script to generate a Cloudformation script for a new EC2 instance in an existing VPC
# Dependencies: troposphere, argparse, cfn_flip

# Standard library imports
import argparse

# Third party imports
from cfn_flip                       import to_yaml
from troposphere.ec2                import Instance
from troposphere                    import Template
from troposphere.cloudformation     import AWSCustomObject

# Custom module imports
from wrappers.cloudformation_stack  import CFStack
from wrappers.boto_client           import boto_client

PARSER = argparse.ArgumentParser(description = 'Generate Cloudformatin for a new EC2 instance in an existing VPC')

### Begin command line arguments
PARSER.add_argument('--region', '-r',
                    help            = "Mandatory. AWS region that you'd like your new instance to live in",
                    required        = True )

PARSER.add_argument('--instance-size', '-is',
                    help            = "Mandatory. Instance size that you'd like to use",
                    required        = True )

PARSER.add_argument('--key-name', '-k',
                    help            = "Optional. SSH key to use for instance bootstrapping",
                    default         = "" )

PARSER.add_argument('--iam-profile', 
                    help            = "Optional. IAM profile to attach to the instance",
                    default         = "" )

PARSER.add_argument('--image-id', '-i', 
                    help            = "Mandatory. Image id to use for the instance", 
                    required        = True )

PARSER.add_argument('--availability-zone', '-az', 
                    help            = "Optional. Availability Zone for the instance" )

PARSER.add_argument('--monitoring', '-m',
                    help            = "Optional. Enable detailed monitoring on the instance",
                    default         = False )

PARSER.add_argument('--subnet', '-s',
                    help            = "Mandatory. Subnet that the instance will live inside.", 
                    required        = True )

PARSER.add_argument('--name', '-n',
                    help            = "Mandatory. Name tag of the instance",
                    required        = True )

PARSER.add_argument('--profile', '-p',
                    help            = "AWS profile that you want to use",
                    default         = "default")

PARSER.add_argument('--stack-name',
                    help            = "Name tag to assign to the stack",
                    required        = True)

PARSER.add_argument('--output', '-o',
                    help            = "Send the generated yaml to stdout",
                    default         = False)

ARGS = PARSER.parse_args()

def generate_template():

    # Initialize a new template
    template = Template()

    # Create the instance definition
    template.add_resource(Instance("Instance",
                        AvailabilityZone        = f"{ARGS.availability_zone}", 
                        IamInstanceProfile      = f"{ARGS.iam_profile}",
                        ImageId                 = f"{ARGS.image_id}",
                        KeyName                 = f"{ARGS.key_name}",
                        Monitoring              = f"{ARGS.monitoring}",
                        SubnetId                = f"{ARGS.subnet}",
                        Tags                    = [{"Key": "Name", "Value": f"{ARGS.name}" }] ))
    
    
    template.add_resource(CustomCidrFinder("CidrFinder",
                        ServiceToken            = 'test',
                        VpcId                   = Ref(VPC),
                        Sizes                   = [24, 25, 26]
                        ))
                        
    template_body = (to_yaml(template.to_json(), clean_up = True))

    # Send the template to stdout and exit
    if ARGS.output:
        print " "
        print template_body
        print " "
        exit()

    # Create a client to cloudformation
    cloudformation_client = boto_client('cloudformation', ARGS.profile, ARGS.region)

    # Instantiate the CF Stack class
    cf_stack = CFStack(template_body, ARGS.stack_name, cloudformation_client)


    print(f"---[ Creating stack {ARGS.stack_name} in region {ARGS.region}")
    cf_stack.deploy_stack()

if __name__ == "__main__":
    generate_template()

