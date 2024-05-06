from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .enums import Role
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role"]

    def validate(self, attrs: dict) -> dict:
        """Change the password for its hash"""

        attrs["password"] = make_password(attrs["password"])

        return attrs


class UserRegistrationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role"]


class UserListCreateAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            UserRegistrationPublicSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserRegistrationPublicSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = UserRegistrationPublicSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.role != Role.ADMIN:
            raise PermissionDenied(
                "Only administrators can perform this action."
            )
        return super().delete(request, *args, **kwargs)


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
