from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from X_app.models import UserCompatibility


class Command(BaseCommand):
    help = 'Update compatibility scores for all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Update compatibility for specific user only',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Number of users to process in each batch',
        )

    def handle(self, *args, **options):
        if options['user']:
            try:
                user = User.objects.get(username=options['user'])
                self.stdout.write(f'Updating compatibility for user: {user.username}')
                UserCompatibility.update_user_compatibilities(user)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated compatibility for {user.username}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User "{options["user"]}" does not exist')
                )
        else:
            self.stdout.write('Updating compatibility scores for all users...')

            users = User.objects.all()
            total_users = users.count()
            processed = 0

            for user in users:
                try:
                    UserCompatibility.update_user_compatibilities(user)
                    processed += 1

                    if processed % options['batch_size'] == 0:
                        self.stdout.write(f'Processed {processed}/{total_users} users...')

                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Error processing user {user.username}: {e}')
                    )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated compatibility for {processed}/{total_users} users')
            )