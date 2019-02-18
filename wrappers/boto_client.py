import boto3

def boto_client(session_type, profile, region_name):
    '''
    Boto3 Session handler

    Parameters:

        session_type (service of aws to create a connection to)
        profile (local aws profile to use to authenticate your connection)
        region_name (aws region to connect to)

    Returns:
    
        boto client object for use with the AWS api
    '''
    
    return boto3.Session(
        
        profile_name            = profile, 
        region_name             = region_name
        
        ).client(session_type)

