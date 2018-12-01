from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone


from users.models import User


class Command(BaseCommand):
    help = 'Removes users from paying_user group if package is expired'

    def handle(self, *args, **options):
        all_users = User.objects.all()
        group = Group.objects.get(name='paying_user')

        for user in all_users:
            if user.profile.sub_expires_on and user.profile.sub_expires_on < timezone.now():
                    user.profile.sub_expires_on = None
                    user.profile.save()
                    group.user_set.remove(user)
                    self.stdout.write("Removed %s from paying_user group" % user)
            else:
                self.stdout.write("No users were moved")

        """
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        """
