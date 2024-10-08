from django.db import models

class Conversation(models.Model):
    user_input = models.TextField()
    response_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_input} - AI: {self.response_text}"

