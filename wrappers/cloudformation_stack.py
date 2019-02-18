# Module that will deploy the generated Cloudformation stack

class CFStack:

    def __init__(self, template_body, stack_name, cloudformation_client):

        self.template_body              = template_body
        self.stack_name                 = stack_name
        self.cloudformation_client      = cloudformation_client

    def deploy_stack(self):
        '''
        Uses the python generated Cloudformation valid yaml to deploy a new CF stack in the region you want.

        Parameters:

        template_body (valid Cloudformation yaml)
        region (aws region to deploy into)
        stack_name (name tag to give the stack)

        Returns:
            nothing
        '''
        
        self.cloudformation_client.create_stack(
                                            StackName       = self.stack_name,
                                            TemplateBody    = self.template_body )
        
        print('---[Waiting for stack creation to complete')
        waiter = self.cloudformation_client.get_waiter('stack_create_complete')
        waiter.wait(StackName = self.stack_name)



        