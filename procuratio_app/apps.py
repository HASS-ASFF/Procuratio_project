from django.apps import AppConfig


class ProcuratioAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'procuratio_app'
    def ready(self):
        import procuratio_app.signals
