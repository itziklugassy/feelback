from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO
from .models import Project, ProjectCategory, Rating
from .serializers import ProjectSerializer, ProjectCategorySerializer, RatingSerializer
from rest_framework.response import Response

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer
    
    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        project = self.get_object()
        ratings = Rating.objects.filter(project=project)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        headers = ['Project', 'User', 'Insight', 'Concept', 'Execution', 'Prominence', 'Pride', 'Originality', 'Date']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        ratings = Rating.objects.all()
        for row, rating in enumerate(ratings, 1):
            worksheet.write(row, 0, rating.project.title)
            worksheet.write(row, 1, rating.user.username)
            worksheet.write(row, 2, rating.insight_score)
            worksheet.write(row, 3, rating.concept_score)
            worksheet.write(row, 4, rating.execution_score)
            worksheet.write(row, 5, rating.prominence_score)
            worksheet.write(row, 6, rating.pride_score)
            worksheet.write(row, 7, rating.originality_score)
            worksheet.write(row, 8, rating.created_at.strftime("%Y-%m-%d %H:%M:%S"))

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=ratings.xlsx'
        return response