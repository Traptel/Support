from django.db.models import Q
from rest_framework import generics, response, serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

from users.enums import Role

from .enums import Status
from .models import Issue, Message


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
        user = self.request.user
        if user.role == Role.ADMIN:
            return Issue.objects.all()
        elif user.role == Role.SENIOR:
            return Issue.objects.filter(
                Q(senior=self.request.user)
                | (Q(senior=None) & Q(status=Status.OPENED))
            )
        elif user.role == Role.JUNIOR:
            return Issue.objects.filter(junior=user)

    def post(self, request):
        if request.user.role == Role.SENIOR:
            raise Exception("The role is senior")

        return super().post(request)


class IssuesRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    lookup_url_kwarg = "id"

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.role != Role.ADMIN:
            raise PermissionDenied(
                "Only administrators can perform this action."
            )
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.role not in [Role.ADMIN, Role.SENIOR]:
            raise PermissionDenied(
                "Only administrators and seniors can perform this action."
            )
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        issue = self.get_object()
        if user.role == Role.JUNIOR and issue.junior != user:
            raise PermissionDenied(
                "You can't access another person's question."
            )
        return super().retrieve(request, *args, **kwargs)


class MessegaSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Message
        fields = "__all__"

    def save(self):
        if (user := self.validated_data.pop("user", None)) is not None:
            self.validated_data["user_id"] = user.id

        if (issue := self.validated_data.pop("issue", None)) is not None:
            self.validated_data["issue_id"] = issue.id

        return super().save()


@api_view(["GET", "POST"])
def messages_api_dispatcher(request: Request, issue_id: int):
    if request.method == "GET":
        # messages = Message.objects.filter(
        # Q(
        #     issue__id=issue_id,
        #     issue__junior = request.user
        # )
        # | Q(
        #     issue__id = issue_id,
        #     issue__senior = request.user
        # )
        messages = Message.objects.filter(
            Q(issue__id=issue_id)
            & (Q(issue__senior=request.user) | Q(issue__junior=request.user))
        ).order_by("-timestamp")
        serializers = MessegaSerializer(messages, many=True)

        return response.Response(serializers.data)
    else:
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id}

        serializer = MessegaSerializer(
            data=payload, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.validated_data)


@api_view(["PUT"])
def issues_close(request: Request, id: int):
    issue = Issue.objects.get(id=id)
    if request.user.role != Role.SENIOR:
        raise PermissionError("Only senior users can close issues")

    if issue.status != Status.IN_PROGRESS:
        raise response.Response(
            {"message": "Issue is not In progress"}, status=422
        )
    else:
        issue.senior = request.user
        issue.status = Status.CLOSED
        issue.save()

    serializers = IssueSerializer(issue)
    return response.Response(serializers.data)


@api_view(["PUT"])
def issues_take(request: Request, id: int):
    issue = Issue.objects.get(id=id)

    if request.user.role != Role.SENIOR:
        raise PermissionError("Only senior users can take issues")

    if (issue.status != Status.OPENED) or (issue.senior is not None):
        return response.Response(
            {"message": "Issue is not Opened or senior is set..."},
            status=422,
        )
    else:
        issue.senior = request.user
        issue.status = Status.IN_PROGRESS
        issue.save()

    serializer = IssueSerializer(issue)

    return response.Response(serializer.data)


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
