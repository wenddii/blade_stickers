from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False, verbose_name="Marked as Read")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
