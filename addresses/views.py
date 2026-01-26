from django.shortcuts import render
from rest_framework import generics
from .models import Address
from .serializers import AddressDetailSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .services import get_user_addresses, set_defult_address

class AddressListView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)


class AddressCreateView(generics.CreateAPIView):
    serializer_class= AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
       address = serializer.save(user = self.request.user)   # Assign the logged-in user as the owner of the address
       if address.is_default:
           set_defult_address(address)   
    
class AddressDetailView(generics.RetrieveAPIView):
    serializer_class = AddressDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)

class AddressUpdateView(generics.UpdateAPIView):
    serializer_class= AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)
    
    def perform_update(self, serializer):
        address = serializer.save()
        if address.is_default:
            set_defult_address(address)

class AddressDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)
    



class AdminAddressListView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAdminUser]


class AdminAddressCreateView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class= AddressSerializer
    permission_classes = [IsAdminUser]

    
    
class AdminAddressDetailView(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressDetailSerializer
    permission_classes = [IsAdminUser]

    

class  AdminAddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class= AddressSerializer
    permission_classes = [IsAdminUser]



class AdminAddressDeleteView(generics.DestroyAPIView):
    queryset = Address.objects.all()
    permission_classes = [IsAdminUser]


