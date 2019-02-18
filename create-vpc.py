# Script that will generate the clouformation for a new VPC in whatever region you want
# Dependencies: troposphere, argparse, cfn_flip

from troposphere     import Template
from troposphere     import Ref
from troposphere     import GetAtt
from troposphere.ec2 import VPC
from troposphere.ec2 import DHCPOptions
from troposphere.ec2 import VPCDHCPOptionsAssociation
from troposphere.ec2 import Subnet
from troposphere.ec2 import InternetGateway
from troposphere.ec2 import VPCGatewayAttachment

from wrappers.boto_client import boto_client
from cfn_flip import to_yaml
import argparse

PARSER = argparse.ArgumentParser(description = 'Generate cloudformation for a new VPC')

### Begin command line arguments
PARSER.add_argument('--region', '-r',
                    help            = "AWS region that you'd like your new VPC to live in",
                    required        = True )

PARSER.add_argument('--name', '-n',
                    help            = "Name tag to assign to the new VPC",
                    required        = True )

PARSER.add_argument('--cidr-block', '-c',
                    help            = "CIDR to use for the new VPC",
                    required        = True )

PARSER.add_argument('--public-access', "-public",
                    help            = "Determines whether or not to make the VPC publicly accessible",
                    default         = False )

PARSER.add_argument('--subnets', '-s',
                    help            = "Subnets to create inside the VPC. Type: space separated list",
                    required        = True,
                    nargs           = '+' )
PARSER.add_argument('--availablity-zones', '-az',
                    help            = "AZ's to create the new subnets in. First az passed in goes to the first subnet, second az to second subnet etc...",
                    required        = True,
                    nargs           = '+' )

PARSER.add_argument('--profile', '-p',
                    help            = "AWS cli profile to use",
                    default         = "default")

ARGS = PARSER.parse_args()
### End command line arguments

def generate_template():
    '''
    Initializes the template object and attaches all the resources to it.
    Then prints the body in yaml after doing some opionionated cleanup.

    ::returns template_body template in yaml format
    ::params  none
    '''

    # Initialize a new CF template
    template  = Template()

    # Create the VPC resource
    template.add_resource(VPC("VPC",
                    CidrBlock           = "%s" % ARGS.cidr_block,
                    EnableDnsSupport    = True,
                    EnableDnsHostnames  = True,
                    Tags                = [{"Key": "Name", "Value": "%s" % ARGS.name }] ))

    # Create a DHCP Options set
    template.add_resource(DHCPOptions("DHCPOptions",
                    DomainNameServers   = ["AmazonProvidedDNS"], 
                    Tags                = [{"Key": "Name", "Value": "%s-dhcp-options" % ARGS.name }] ))
    
    # Associate the DHCP Options set with the VPC
    template.add_resource(VPCDHCPOptionsAssociation("DHCPAssociation",
                    DhcpOptionsId       = Ref("DHCPOptions"), 
                    VpcId               = Ref("VPC") ))

    # Determine if public access is needed. If so, attach an IGW to the VPC
    if ARGS.public_access:
        template.add_resource(InternetGateway("IGW",
                    Tags                = [{"Key": "Name", "Value": "%s-igw" % ARGS.name }] ))
        
        template.add_resource(VPCGatewayAttachment("IGWAttachment",
                    InternetGatewayId   = Ref("IGW"),
                    VpcId               = Ref("VPC") ))
    
    # Join subnets + az lists together and create subnet resources
    for index, subnets in enumerate(zip(ARGS.subnets, ARGS.availablity_zones)):
        template.add_resource(Subnet("Subnet%s" % (index),
                    AvailabilityZone    = subnets[1],
                    CidrBlock           = subnets[0],
                    VpcId               = Ref("VPC") ))


    template_body = (to_yaml(template.to_json(), clean_up = True))

    return template_body

print " "
print generate_template()

