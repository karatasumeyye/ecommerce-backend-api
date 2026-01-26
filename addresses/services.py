from .models import Address
from rest_framework.exceptions import ValidationError

def get_user_addresses(user):
    return Address.objects.filter(user=user)

def set_defult_address(address):
    Address.objects.filter(user=address.user, is_default=True).update(is_default=False)  # Unset previous default address
    address.is_default = True
    address.save()

def get_user_adress_or_404(user,address_id):
    try:
        return Address.objects.get(id=address_id, user= user)
    except Address.DoesNotExist:
        raise ValidationError("Address not found for this user.")
