import asyncio
import csv
from typing import List, Dict, Optional, Union, Annotated
import networkx as nx


class File:
    def __init__(self, path):
        self.__path: str = path
        self.__file = list()
        self.__upload_file()

    def __upload_file(self):
        f = open(self.__path, newline="")
        self.__file = list(csv.reader(f, delimiter='\t', quotechar='"'))
        self.__file.pop(0)
        for line in self.__file:
            line[2] = int(line[2])
            line[3] = int(line[3])

    def get(self):
        return self.__file


class Reader:
    def __init__(self, path):
        self.file = File(path).get()

    async def get_from(self):
        """
        Получаем список из городов отбытия
        :return:
        """
        return list({i[0] for i in self.file})

    async def get_to(self):
        """
        Получаем список из городов прибытия
        :return:
        """
        return list({i[1] for i in self.file})


class Graph:
    def __init__(self, path):
        self.file = File(path).get()
        self.graph = nx.Graph()
        self.fill_graph()

    def fill_graph(self):
        """
        заполняем граф по значениям из файла
        :return:
        """
        for i in self.file:
            self.graph.add_edge(i[0], i[1], cost=int(i[2]), days=int(i[3]))

    def get(self):
        return self.graph

class WayDirector:
    def __init__(self, path, from_, to):
        self.path = path
        self.from_ = from_
        self.to = to
        self.graph = Graph(path).get()

    async def calculate_routes(self, weight, str_weight)->Dict:
        if self.from_ not in self.graph or self.to not in self.graph:
            raise ValueError(f"Города {self.from_} или {self.to} отсутствуют в графе.")
        try:
            # Расчет самого экономичного маршрута
            cost_path = nx.shortest_path(self.graph, source=self.from_, target=self.to, weight=weight)
            cost = sum(self.graph[cost_path[i]][cost_path[i + 1]]['cost'] for i in range(len(cost_path) - 1))
            days = sum(self.graph[cost_path[i]][cost_path[i + 1]]['days'] for i in range(len(cost_path) - 1))
            return {"type": str_weight, "cost": cost, "days": days, "path": cost_path}
        except nx.NetworkXNoPath:
            return {"type": self, "error": "Нет доступного пути."}
