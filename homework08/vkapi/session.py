import typing as tp

import requests  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.packages.urllib3.util.retry import Retry  # type: ignore


class Session:
    _adapter: HTTPAdapter  # Объявление приватного поля _adapter типа HTTPAdapter
    _request_session: requests.Session  # Объявление приватного поля _request_session типа requests.Session
    _base_url: str  # Объявление приватного поля _base_url типа str
    _timeout: float  # Объявление приватного поля _timeout типа float
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self._request_session = requests.Session()  # Создание объекта сеанса запроса
        # Создание адаптера с настройками повторных запросов
        adapter = HTTPAdapter(
            max_retries=Retry(
                backoff_factor=backoff_factor,
                total=max_retries,
                status_forcelist=[500, 502, 503, 504],
            )
        )
        # Привязка адаптера к URL-префиксу "https://"
        self._request_session.mount(prefix="https://", adapter=adapter)

        self._timeout = timeout  # Присвоение значения timeout приватному полю _timeout
        self._base_url = base_url  # Присвоение значения base_url приватному полю _base_url

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        """
        Выполняет HTTP-запрос методом GET.

        :param url: Относительный URL запроса.
        :param args: Позиционные аргументы.
        :param kwargs: Именованные аргументы.
        :return: Объект requests.Response.
        """
        full_url = f"{self._base_url}/{url}"  # Формирование полного URL
        # Выполнение GET-запроса
        response = self._request_session.get(url=full_url, params=kwargs, timeout=self._timeout)

        return response

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        """
        Выполняет HTTP-запрос методом POST.

        :param url: Относительный URL запроса.
        :param args: Позиционные аргументы.
        :param kwargs: Именованные аргументы.
        :return: Объект requests.Response.
        """
        full_url = f"{self._base_url}/{url}"  # Формирование полного URL
        # Выполнение POST-запроса
        response = self._request_session.post(url=full_url, data=kwargs, timeout=self._timeout)

        return response
