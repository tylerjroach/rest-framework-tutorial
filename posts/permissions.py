from rest_framework import permissions

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to edit it.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner of the snippet
		return obj.owner == request.user

class IsOwner(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to view or edit it.
	Model instances are expected to include an `owner` attribute.
	"""

	def has_object_permission(self, request, view, obj):

		return obj.id == request.user.id

class IsOwnerModAllCreateGetAuth(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to view or edit it.
	Model instances are expected to include an `owner` attribute.
	"""

	def has_permission(self, request, view):
		if request.method == 'POST':
			return True
		if request.method == 'GET' and request.user.is_authenticated():
			return True
		else:
			return False

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS and request.user.is_authenticated():
			return True
		elif request.method == 'PUT' or request.method == 'PATCH' and request.user.is_authenticated():
			return obj.id == request.user.id
		else:
			return False