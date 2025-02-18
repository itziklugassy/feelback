from django.db import models
from users.models import CustomUser, Department

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    media_url = models.URLField(max_length=500, null=True, blank=True, help_text="YouTube video URL")
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', null=True, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    insight_score = models.IntegerField()
    concept_score = models.IntegerField()
    execution_score = models.IntegerField()
    prominence_score = models.IntegerField()
    pride_score = models.IntegerField()
    originality_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'user']

    def __str__(self):
        return f"{self.user.username}'s rating for {self.project.title}"