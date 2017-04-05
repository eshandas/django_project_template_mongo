from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mongoauth.api_authentications import (
    SessionAuthenticationUnsafeMethods,
    CsrfExemptSessionAuthentication,
)

from .constants import (
    SuccessMessages,
    FailureMessages,
)

from .mongomodels import (
    Post,
)

from .serializers import (
    PostSerializer,
)

from utils.response_handler import generic_response


class PostAPI(APIView):
    authentication_classes = (SessionAuthenticationUnsafeMethods, )
    serializer_class = PostSerializer

    def get(self, request, post_id):
        """
        Gets a particular post
        """
        try:
            posts = Post.objects.get(id=post_id)
            serializer = self.serializer_class(posts)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
                generic_response(FailureMessages.POST_NOT_FOUND),
                status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        """
        Deletes a particular post
        """
        try:
            Post.objects.get(id=post_id).delete()
            return Response(
                generic_response(SuccessMessages.POST_DELETE_SUCCESS),
                status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
                generic_response(FailureMessages.POST_NOT_FOUND),
                status=status.HTTP_404_NOT_FOUND)


class PostsAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    serializer_class = PostSerializer

    def get(self, request):
        """
        Gets all the posts
        """
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a post

        Data:

            {
                "title": "Test Post",
                "body": "<h1>Hello people</h1>",
                "isActive": true
            }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                generic_response(SuccessMessages.POST_SAVE_SUCCESS),
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_406_NOT_ACCEPTABLE)
