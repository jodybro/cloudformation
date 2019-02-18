def boto_client(session_type):
    '''
    Boto3 Session handler
    '''
    
    # If keys were passed, use those
    if ACCESSKEY and SECRETKEY:

        return boto3.Session(

            aws_access_key_id       = ACCESSKEY,
            aws_secret_access_key   = SECRETKEY, 
            region_name             = region_name
            
            ).client(session_type)

    else:
        return boto3.Session(
            
            profile_name            = PROFILE, 
            region_name             = region_name
            
            ).client(session_type)
