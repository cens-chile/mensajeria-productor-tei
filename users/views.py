import logging

from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from users.serializers import UserSerializer, GroupSerializer, CheckSerializer, LogoutSerializer, \
    LogoutRefreshSerializer

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(message)s', datefmt='%d/%b/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

class IsAdminOrSender(permissions.BasePermission):
    """
    Sender permission
    """

    def has_permission(self, request, view):
        return bool(request.user and
                    (request.user.sender or
                    request.user.is_staff))


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['sender'] = user.groups.filter(name="sender").exists()
        # ...

        return token


class MyTokenViewBase(TokenViewBase):
    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        data = {}
        is_refresh = request.path.endswith('/refresh/')
        if is_refresh:
            token_data = request.data
            if 'refresh' not in token_data:
                raise InvalidToken("refresh token not present")
            data['refresh'] = token_data['refresh']
        else:
            data = request.data
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        return response


class MyTokenRefreshSerializer(Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)

        return data


class MyTokenObtainPairView(MyTokenViewBase):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(MyTokenViewBase):
    serializer_class = MyTokenRefreshSerializer

@extend_schema(
    request=None,
    responses=CheckSerializer
)
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def check(request):
    return Response({'status':'ok'}, status=status.HTTP_200_OK)

@extend_schema(
    exclude=True
)
@api_view(['GET'])
def redirect_to_swagger(request):
    return redirect('swagger-ui')

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_data(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    request=LogoutRefreshSerializer,
    responses=LogoutSerializer
)
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    def get_user(user_id=None):
        if user_id is None:
            return False
        return User.objects.get(id=user_id)

    def is_token_owner(user_token, user_request):
        return user_token.username == user_request.username

    token_data = request.data
    if 'refresh' not in token_data:
        raise InvalidToken("refresh token not present")
    try:
        token = RefreshToken(token_data['refresh'])
    except TokenError as e:
        return Response({"details": "{}".format(str(e))}, status=status.HTTP_412_PRECONDITION_FAILED)
    if 'user_id' in token:
        user = get_user(token['user_id'])
        if not user or not is_token_owner(user, request.user):
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        token.blacklist()
        return Response({"details": "blacklisted"}, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response(str(e), status=status.HTTP_401_UNAUTHORIZED)