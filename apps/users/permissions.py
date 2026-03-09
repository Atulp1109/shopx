from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "ADMIN"


class IsMerchant(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "MERCHANT"


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "CUSTOMER"