from django.http.response import JsonResponse

# 404 error
def error_404(request,exception=None):
    message='end point not found'
    response =JsonResponse(data={'message':message,'status_code':404})
    response.status_code=404
    return response
# 500 error
def error_500(request):
    message='somthing wrong in server'
    response =JsonResponse(data={'message':message,'status_code':500})
    response.status_code=500
    return response
# 404 error
def error_400(request,exc):
    message='end point not found'
    response =JsonResponse(data={'message':message,'status_code':404})
    response.status_code=404
    return response