from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


@api_view(["GET"])
def fetch_issues(request):
    all_issues = Issue.objects.all()
    serialized_issues = IssueSerializer(all_issues, many=True)
    return Response(serialized_issues.data)


@api_view(["POST"])
def add_new_issue(request):
    received_data = request.data
    new_issue_serializer = IssueSerializer(data=received_data)

    if new_issue_serializer.is_valid():
        new_issue_serializer.save()
        return Response(new_issue_serializer.data)
    else:
        return Response(new_issue_serializer.errors)
