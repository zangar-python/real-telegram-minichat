import tempfile
import os
import openpyxl
from celery import shared_task

@shared_task
def generate_report_task(data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Report"

    if data:
        ws.append(list(data[0].keys()))
    for row in data:
        ws.append(list(row.values()))

    # создаём безопасный временный файл
    tmp_dir = tempfile.gettempdir()  # на Windows даст что-то вроде C:\Users\Имя\AppData\Local\Temp
    file_path = os.path.join(tmp_dir, f"report_{generate_report_task.request.id}.xlsx")

    wb.save(file_path)
    return file_path
