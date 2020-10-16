from django.core.management.base import BaseCommand
from tg_bot.views import bot


class Command(BaseCommand):
    help = 'Запуск telegram бота локально'

    def handle(self, *args, **kwargs):
        bot.skip_pending = True
        bot.remove_webhook()
        self.stdout.write(self.style.SUCCESS('tg_bot запущен локально...'))
        bot.polling(none_stop=True, interval=0)
