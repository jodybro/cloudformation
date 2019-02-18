# Module that will deploy the generated Cloudformation stack

def deploy_stack(template_body, region, stack_name):
    '''
    Uses the python generated Cloudformation valid yaml to deploy a new CF stack in the region you want.

    Parameters:

     template_body (valid Cloudformation yaml)
     region (aws region to deploy into)
     stack_name (name tag to give the stack)

    Returns:

        nothing
    '''
    
    cloudformation_client.create_stack(
            StackName       = stack_name,
            TemplateBody    = template_body
    )
