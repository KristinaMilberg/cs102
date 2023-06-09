import datetime as dt
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id, fields=["bdate"])
    ages = []
    for friend in friends.items:
        if "bdate" in friend:  # type: ignore
            bdate = friend["bdate"]  # type: ignore
            try:
                birth_year = int(bdate[-4:])
                current_year = dt.date.today().year
                age = current_year - birth_year
                ages.append(age)
            except ValueError:
                pass
    if ages:
        return sum(ages) / len(ages)
    else:
        return None
