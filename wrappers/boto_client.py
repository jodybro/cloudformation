import boto3

def boto_client(session_type, profile, region_name):
    '''
    Boto3 Session handler
    '''
    
    return boto3.Session(
        
        profile_name            = profile, 
        region_name             = region_name
        
        ).client(session_type)

