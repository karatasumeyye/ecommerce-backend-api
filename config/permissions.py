from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_api_key.models import APIKey

class HasValidAPIKey(BasePermission):

    def has_valid_api_key(self,request):
        key = request.headers.get('X-API-KEY')

        if not key:
            raise AuthenticationFailed('API key did not found in request headers.')
        
        try:
            api_key_obj = APIKey.objects.get_from_key(key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key.')
        
        request.auth = api_key_obj
        return True
    
    def has_permission(self, request, view):
        return self.has_valid_api_key(request)
    
class IsAuthenticatedWithAPIKey(HasValidAPIKey):
    def has_permission(self, request, view):
        self.has_valid_api_key(request)

        user = request.user
        if not user or not user.is_authenticated:
            return AuthenticationFailed('Authentication is not successful.')
        
        return True
    

class IsAdminWithAPIKey(HasValidAPIKey):
    def has_permission(self, request, view):
        self.has_valid_api_key(request)

        user = request.user
        if not user or not user.is_staff:
            return AuthenticationFailed('Only admin users are allowed to perform this action.')
        
        return True