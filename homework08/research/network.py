import typing as tp
from collections import defaultdict

import community  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore
import pandas as pd  # type: ignore

from vkapi.friends import get_friends, get_mutual


def ego_network(
    user_id: tp.Optional[int] = None, friends: tp.Optional[tp.List[int]] = None
) -> tp.List[tp.Tuple[int, int]]:
    """
    Построить эгоцентричный граф друзей.

    :param user_id: Идентификатор пользователя, для которого строится граф друзей.
    :param friends: Идентификаторы друзей, между которыми устанавливаются связи.
    """
    if friends is None:  # Если идентификаторы друзей не указаны
        # получаем список друзей пользователя user_id с указанием поля "nickname"
        friends = get_friends(user_id=user_id, fields=["nickname"]).items # type: ignore
        # Инициализируем список active_friends для хранения идентификаторов активных друзей.
        # Проходимся по каждому другу в списке друзей и проверяем, является ли он активным
        # (не деактивирован и не закрытый профиль).
        # Добавляем идентификаторы активных друзей в список active_friends.
        active_friends = [user["id"] for user in friends if not user.get("deactivated") and not user.get("is_closed")] # type: ignore
    else:
        # Если friends указан, присваиваем active_friends значение friends.
        active_friends = friends  # type: ignore
    # Получаем список общих друзей между пользователем user_id и друзьями из списка active_friends.
    items = get_mutual(source_uid=user_id, target_uids=active_friends)
    net = []  # Инициализируем пустой список net для хранения связей в графе.
    for item in items:  # Проходимся по каждому элементу в списке items.
        # Расширяем список net парами (item["id"], mutual), где item["id"] - идентификатор пользователя, а mutual - идентификатор общего друга.
        net.extend([(item["id"], mutual) for mutual in item["common_friends"]]) # type: ignore
    # Возвращаем список связей в графе net.
    return net


def plot_ego_network(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    nx.draw(graph, layout, node_size=10, node_color="black", alpha=0.5)
    plt.title("Ego Network", size=15)
    plt.show()


def plot_communities(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    partition = community.community_louvain.best_partition(graph)
    nx.draw(graph, layout, node_size=25, node_color=list(partition.values()), alpha=0.8)
    plt.title("Ego Network", size=15)
    plt.show()


def get_communities(net: tp.List[tp.Tuple[int, int]]) -> tp.Dict[int, tp.List[int]]:
    communities = defaultdict(list)
    graph = nx.Graph()
    graph.add_edges_from(net)
    partition = community.community_louvain.best_partition(graph)
    for uid, cluster in partition.items():
        communities[cluster].append(uid)
    return communities


def describe_communities(
    clusters: tp.Dict[int, tp.List[int]],
    friends: tp.List[tp.Dict[str, tp.Any]],
    fields: tp.Optional[tp.List[str]] = None,
) -> pd.DataFrame:
    if fields is None:
        fields = ["first_name", "last_name"]

    data = []
    for cluster_n, cluster_users in clusters.items():
        for uid in cluster_users:
            for friend in friends:
                if uid == friend["id"]:
                    data.append([cluster_n] + [friend.get(field) for field in fields])
                    break
    return pd.DataFrame(data=data, columns=["cluster"] + fields)
