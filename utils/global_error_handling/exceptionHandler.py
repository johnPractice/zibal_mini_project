from rest_framework.views import exception_handler

def custom_excepception_handler(exc,context):
    handlers={
        'ValidationError':_handel_generic_error,
        'Http404':_handel_generic_error,
        'PermissionDenied ':_handel_generic_error,
        'NotAuthenticated':_handel_generic_error,
    }
    response=exception_handler(exc,context)

    if response is not None:
        response.data['status_code']=response.status_code
    exception_class=exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc,context,response)
    return response


# private methode
def _handel_generic_error(exc,context,response):
    return response



