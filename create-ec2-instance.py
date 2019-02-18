# Script to generate a Cloudformation script for a new EC2 instance in an existing VPC
# Dependencies: troposphere, argparse, cfn_flip

from cfn_flip        import to_yaml
from troposphere.ec2 import Instance
from troposphere     import Template

import argparse

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

ARGS = PARSER.parse_args()


def generate_template():

    # Initialize a new template
    template = Template()

    # Create the instance definition
    template.add_resource(Instance("Instance",
                        AvailabilityZone        = "%s" % (ARGS.availability_zone), 
                        IamInstanceProfile      = "%s" % (ARGS.iam_profile),
                        ImageId                 = "%s" % (ARGS.image_id),
                        KeyName                 = "%s" % (ARGS.key_name),
                        Monitoring              = "%s" % (ARGS.monitoring),
                        SubnetId                = "%s" % (ARGS.subnet),
                        Tags                    = [{"Key": "Name", "Value": "%s" % ARGS.name }] ))
                        
    template_body = (to_yaml(template.to_json(), clean_up = True))
    return template_body

print " "
print generate_template()



                