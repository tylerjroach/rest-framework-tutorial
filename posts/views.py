from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from posts.models import Post
from posts.permissions import IsOwnerOrReadOnly, IsOwnerModAllCreateGetAuth
from posts.serializers import PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
	"""
	This endpoint presents daily posts.

	The **owner** of the daily post may update or delete instances
	of the post.

	"""

	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
						  IsOwnerOrReadOnly,)

	@detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
	def highlight(self, request, *args, **kwargs):
		post = self.get_object()
		return Response(post.highlighted)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
	
	
class UserViewSet(viewsets.ModelViewSet):
	"""
	This endpoint presents the users in the system.

	As you can see, the collection of post instances owned by a user are
	serialized using a hyperlinked representation.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
	permission_classes = (IsOwnerModAllCreateGetAuth,)
	
