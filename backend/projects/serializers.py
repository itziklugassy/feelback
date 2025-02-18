from rest_framework import serializers
from .models import Project, ProjectCategory, Rating

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'project', 'insight_score', 'concept_score', 
                 'execution_score', 'prominence_score', 'pride_score', 
                 'originality_score']
        read_only_fields = ['user']