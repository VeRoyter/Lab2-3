import pandas as pd
from django.core.management.base import BaseCommand
from main.models import Show, Country, Director, CountriesCast, DirectorsCast
import os

class Command(BaseCommand):
    help = 'Загружает дополнительные данные (Director, Country) из CSV'

    def handle(self, *args, **options):
        # Путь к файлу. Так как запускаем через manage.py, путь будет от корня проекта
        csv_path = 'netflix_titles_CLEANED.csv'

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'Файл не найден: {csv_path}'))
            return

        self.stdout.write("Начинаем чтение CSV...")
        df = pd.read_csv(csv_path)

        count_dirs = 0
        count_countries = 0

        # Получаем все шоу сразу, чтобы не делать запросы в цикле (оптимизация)
        # Создаем словарь {title: show_object}
        self.stdout.write("Кэширование шоу из БД...")
        all_shows = Show.objects.all()
        shows_dict = {show.title: show for show in all_shows}

        self.stdout.write("Начинаем импорт...")

        for index, row in df.iterrows():
            title = row['title']
            
            # Получаем шоу из словаря (быстрее, чем запрос к БД)
            show = shows_dict.get(title)
            
            if not show:
                continue

            # --- Обработка режиссеров ---
            if pd.notna(row['directors']):
                directors_list = str(row['directors']).split(',')
                for director_name in directors_list:
                    d_name = director_name.strip()
                    if d_name:
                        director_obj, created = Director.objects.get_or_create(
                            director_name=d_name
                        )
                        DirectorsCast.objects.get_or_create(
                            show=show,
                            director=director_obj
                        )
                        if created: count_dirs += 1

            # --- Обработка стран ---
            if pd.notna(row['countries']):
                countries_list = str(row['countries']).split(',')
                for country_name in countries_list:
                    c_name = country_name.strip()
                    if c_name:
                        country_obj, created = Country.objects.get_or_create(
                            country_name=c_name
                        )
                        CountriesCast.objects.get_or_create(
                            show=show,
                            country=country_obj
                        )
                        if created: count_countries += 1
            
            if index % 500 == 0:
                self.stdout.write(f"Обработано {index} строк...")

        self.stdout.write(self.style.SUCCESS(f'ГОТОВО! Добавлено режиссеров: {count_dirs}, стран: {count_countries}'))


# SELECT COUNT(*) FROM "Shows";
# SELECT COUNT(*) FROM "Country";
# SELECT COUNT(*) FROM "Director";
# SELECT COUNT(*) FROM "Actor";
# SELECT COUNT(*) FROM "Countries Cast";
# SELECT COUNT(*) FROM "Directors Cast";
# SELECT COUNT(*) FROM "Actors Cast";