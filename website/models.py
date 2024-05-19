from django.db import models

from django.contrib.auth.models import User

class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_text = models.TextField()
    summarized_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Summary by {self.user.username} on {self.created_at}'
