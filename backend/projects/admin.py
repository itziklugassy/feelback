from django.contrib import admin 
from django.db.models import Avg, Count, Sum
from django.urls import path
from django.template.response import TemplateResponse
from .models import Project, ProjectCategory, Rating
import json

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
   list_display = ('title', 'category', 'total_ratings', 'total_score', 'average_rating', 'created_at', 'is_active')
   list_filter = ('category', 'is_active')
   search_fields = ('title', 'description')

   def get_urls(self):
       urls = super().get_urls()
       custom_urls = [
           path('analytics/', self.admin_site.admin_view(self.analytics_view), name='project-analytics'),
       ]
       return custom_urls + urls

   def analytics_view(self, request):
       projects = Project.objects.all()
       project_ratings = {
           'labels': json.dumps([p.title for p in projects]),
           'total_scores': json.dumps([self.total_score(p) for p in projects]),
           'avg_scores': json.dumps([self.average_rating(p) for p in projects]),
           'total_votes': json.dumps([self.total_ratings(p) for p in projects]),
       }
       
       context = {
           'title': 'ניתוח פרויקטים',
           'projects_data': [{
               'title': project.title,
               'total_ratings': Rating.objects.filter(project=project).count(),
               'total_score': self.total_score(project),
               'avg_scores': Rating.objects.filter(project=project).aggregate(
                   insight=Avg('insight_score'),
                   concept=Avg('concept_score'),
                   execution=Avg('execution_score'),
                   prominence=Avg('prominence_score'),
                   pride=Avg('pride_score'),
                   originality=Avg('originality_score')
               )
           } for project in projects],
           'chart_data': project_ratings
       }
       return TemplateResponse(request, 'admin/project_analytics.html', context)

   def total_ratings(self, obj):
       return Rating.objects.filter(project=obj).count()
   total_ratings.short_description = 'מספר דירוגים'

   def total_score(self, obj):
       totals = Rating.objects.filter(project=obj).aggregate(
           insight=Sum('insight_score'),
           concept=Sum('concept_score'),
           execution=Sum('execution_score'),
           prominence=Sum('prominence_score'),
           pride=Sum('pride_score'),
           originality=Sum('originality_score')
       )
       return sum(v for v in totals.values() if v is not None)
   total_score.short_description = 'ציון כולל'
   
   def average_rating(self, obj):
       avgs = Rating.objects.filter(project=obj).aggregate(
           insight=Avg('insight_score'),
           concept=Avg('concept_score'),
           execution=Avg('execution_score'),
           prominence=Avg('prominence_score'),
           pride=Avg('pride_score'),
           originality=Avg('originality_score')
       )
       valid_scores = [v for v in avgs.values() if v is not None]
       return round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else 0
   average_rating.short_description = 'ציון ממוצע'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
   list_display = ('project', 'user', 'created_at', 'average_score', 'total_score')
   list_filter = ('project', 'user', 'created_at')
   search_fields = ('project__title', 'user__username')

   def average_score(self, obj):
       scores = [
           obj.insight_score,
           obj.concept_score,
           obj.execution_score,
           obj.prominence_score,
           obj.pride_score,
           obj.originality_score
       ]
       return round(sum(scores) / len(scores), 2)
   average_score.short_description = 'ציון ממוצע'

   def total_score(self, obj):
       return sum([
           obj.insight_score,
           obj.concept_score,
           obj.execution_score,
           obj.prominence_score,
           obj.pride_score,
           obj.originality_score
       ])
   total_score.short_description = 'ציון כולל'

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
   list_display = ('name', 'created_at')
   search_fields = ('name', 'description')