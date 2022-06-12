"""
signals
"""


def create_custom_user(sender, instance, signal, created, **kwargs):
    """When user is created also create a custom user."""
    from routes.user.models import Climber

    if created:
        Climber.objects.create(user=instance)
    instance.gpsfunuser.save()
