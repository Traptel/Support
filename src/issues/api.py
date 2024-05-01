from rest_framework import generics, serializers

from users.enums import Role

from .enums import Status
from .models import Issue


class IssueSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    junior = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = "__all__"

    def validate(self, attrs):
        attrs["status"] = Status.OPEND
        return attrs


class IssueAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()

    def post(self, request):
        if request.user.role == Role.SENIOR:
            raise Exception("The role is senior")

        return super().post(request)


class IssuesRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    lookup_url_kwarg = "id"


# @api_view(["GET"])
# def fetch_issues(request):
#     all_issues = Issue.objects.all()
#     serialized_issues = IssueSerializer(all_issues, many=True)
#     return Response(serialized_issues.data)


# @api_view(["POST"])
# def add_new_issue(request):
#     received_data = request.data
#     new_issue_serializer = IssueSerializer(data=received_data)

#     if new_issue_serializer.is_valid():
#         new_issue_serializer.save()
#         return Response(new_issue_serializer.data)
#     else:
#         return Response(new_issue_serializer.errors)
