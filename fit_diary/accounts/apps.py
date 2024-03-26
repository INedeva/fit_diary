from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fit_diary.accounts'

    def ready(self):
        import fit_diary.accounts.signals