from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import generate_report_task
from celery.result import AsyncResult
from rest_framework.permissions import AllowAny


class GenerateReportView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.get("rows", [])
        task = generate_report_task.delay(data)
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class TaskStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, task_id):
        result = AsyncResult(task_id)

        if result.successful():
            return Response(
                {"status": "completed", "file_path": result.result},
                status=status.HTTP_200_OK,
            )
        elif result.failed():
            # Ошибка при выполнении задачи
            return Response(
                {"status": "failed", "error": str(result.result)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        elif result.status == "PENDING":
            return Response({"status": "pending"}, status=status.HTTP_202_ACCEPTED)
        else:
            # В процессе (STARTED, RETRY и т.д.)
            return Response({"status": result.status}, status=status.HTTP_200_OK)
