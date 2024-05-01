from django.contrib.auth.hashers import make_password
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "role",
            "is_active",
        ]

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])
        return attrs


class UserAPI(generics.ListAPIView):
    http_method_names = ["get"]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserRegistrationAPI(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()


class UserRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"


# def create_user(request: HttpRequest) -> JsonResponse:
#     if request.method != "POST":
#         raise NotImplementedError("Only POST requsts")

#     data: dict = json.loads(request.body)
#     user = User.objects.create_user(**data)

#     results = {
#         "id": user.id,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "role": user.role,
#         "is_active": user.is_active,
#     }

#     return JsonResponse(results)
