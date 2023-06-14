import datetime as dt
import typing as tp

from vkapi.friends import get_friends

# Импортируем функцию get_friends из модуля vkapi.friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    # Получаем список друзей пользователя, используя функцию get_friends с параметром user_id и дополнительным полем "bdate"
    friends = get_friends(user_id, fields=["bdate"])
    ages = []  # Создаем пустой список ages для хранения возрастов друзей
    for friend in friends.items:  # Итерируемся по каждому другу пользователя в списке friends
        # Проверяем, содержит ли друг поле "bdate"
        if "bdate" in friend:  # type: ignore
            # Получаем дату рождения друга из поля "bdate"
            bdate = friend["bdate"]  # type: ignore
            try:
                # Получаем год рождения из даты рождения
                # Извлекаем последние 4 символа из строки bdate и преобразуем их в целое число
                birth_year = int(bdate[-4:])
                current_year = dt.date.today().year  # Получаем текущий год из объекта даты сегодняшнего дня
                age = current_year - birth_year  # Вычисляем возраст, вычитая год рождения из текущего года
                ages.append(age)  # Добавляем возраст в список ages
            except ValueError:
                pass
            # Если происходит ошибка ValueError (например, при некорректной дате рождения), игнорируем ее и переходим к следующему другу
    if ages:
        # Если список ages не пуст, возвращаем среднее значение возрастов из списка
        return sum(ages) / len(ages)
    else:
        return None
    # Если список ages пуст, возвращаем None (отсутствие данных о возрасте)
