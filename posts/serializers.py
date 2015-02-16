from rest_framework import serializers
from posts.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.HyperlinkedModelSerializer):
	userId = serializers.ReadOnlyField(source='owner.id')
	username = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Post
		fields = ('userId', 'username', 'title', 'description')
	
			  
class UserSerializer(serializers.ModelSerializer):

	
	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'email')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(
			email=validated_data['email'],
			username=validated_data['username']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

	def update(self, instance, validated_data):
		instance.email = validated_data.get('email', instance.email)
		instance.save()
		return instance
