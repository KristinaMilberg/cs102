import dataclasses
import math
import time
import typing as tp
from typing import List, Optional


from vkapi import session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    """
    Ответ на вызов метода `friends.get`.

    :param count: Количество пользователей.
    :param items: Список идентификаторов друзей пользователя или список пользователей.
    """

    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: Optional[List[str]] = None
) -> FriendsResponse:
    """
    Получить список друзей пользователя.

    :param user_id: Идентификатор пользователя.
    :param count: Количество друзей для получения.
    :param offset: Смещение списка друзей.
    :param fields: Список полей, которые нужно получить о каждом друге.
    :return: Ответ на вызов метода `friends.get` с количеством пользователей и списком идентификаторов друзей.
    """
    # Отправляем запрос к API VK с помощью метода GET.
    # Параметры запроса включают идентификатор пользователя, количество друзей, смещение, поля и токен доступа.

    response = session.get(
        "friends.get",
        user_id=user_id,
        count=count,
        offset=offset,
        fields=fields,
        access_token=VK_CONFIG["access_token"],
        v=VK_CONFIG["version"],
    )
    # Отправляем GET-запрос к API VK с указанными параметрами и получаем ответ
    # Проверяем статус кода ответа. Если 200, то успешный запрос.
    try:
        # Получаем данные из JSON-ответа.
        data = response.json()
        # Извлекаем значение поля count из данных
        count = data["response"]["count"]
        # Извлекаем значение поля items из данных
        items = data["response"]["items"]
        # Возвращаем объект FriendsResponse с количеством пользователей и списком идентификаторов друзей.
        return FriendsResponse(count=count, items=items)
    except Exception as e:
        raise APIError.bad_request(message=str(e))
    # В случае возникновения исключения, вызываем исключение APIError с сообщением об ошибке


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def _get_mutual_list_from_api(session, query_params) -> tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]:
    mutual_list = []
    # Итерируемся в соответствии с количеством запросов
    for _ in range(query_params["requests_count"]):
        # Отправляем GET-запрос к API VK с указанными параметрами и получаем ответ
        response = session.get(
            "friends.getMutual",
            source_uid=query_params["source_uid"],
            target_uid=query_params["target_uid"],
            target_uids=",".join(str(uid) for uid in query_params["target_uids"])
            if query_params["target_uids"]
            else None,
            order=query_params["order"],
            count=query_params["count"],
            offset=query_params["offset"],
            v="5.131",
            access_token=VK_CONFIG["access_token"],
        )
        # Получаем данные из JSON-ответа
        if response.status_code == 200:
            response_data = response.json()["response"]
            # Добавляем полученные данные в список mutual_list
            mutual_list.extend(response_data)
        # Увеличиваем значение смещения в параметрах запроса на 100
        query_params["offset"] += 100
        # Задержка в выполнении для соблюдения ограничений API
        time.sleep(1)

    return mutual_list


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    # Формируем словарь query_params с заданными параметрами запроса
    query_params = {
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": target_uids,
        "order": order,
        "count": count,
        "offset": offset,
        "progress": progress,
        "requests_count": 1,
    }
    # Если заданы идентификаторы целевых пользователей, определяем количество запросов на основе их количества
    if target_uids is not None:
        target_limit = 100
        assert isinstance(target_limit, int)
        query_params["requests_count"] = math.ceil(len(target_uids) / target_limit)
    # Вызываем функцию _get_mutual_list_from_api для получения списка взаимных друзей
    mutual_list = _get_mutual_list_from_api(session, query_params)
    try:
        # Преобразуем список взаимных друзей в список объектов MutualFriends, если возможно,
        mutual_friends_list = [MutualFriends(**item) for item in mutual_list]  # type: ignore
    except TypeError:
        # иначе возвращаем исходный список
        return mutual_list  # type: ignore

    return mutual_friends_list
