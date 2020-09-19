def retry_policy(backoff):
    """
    Compatible policy for :code:`twisted.application.internet.ClientService`
    # The attempts either
    # * Increase by one
    # * Reset to 0
    def ret_value(attempts):
        if attempts == 0:
            reset(backoff)
        return next(backoff) 
