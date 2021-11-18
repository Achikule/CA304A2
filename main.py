#!usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI(title="Alen Joy CA304 Assessment 2")


class Router(BaseModel):
    name: str


class RouterConnection(BaseModel):
    routerFrom: str
    routerTo: str
    routerDist: Optional[int]


class RouterGraph:
    def __init__(self):
        self.vertices = {}
        self.matrix = []

    def __len__(self):
        return len(self.vertices.keys())

    def print_matrix(self):
        return self.matrix

    def add_router(self, name):
        if name not in self.vertices.keys():
            self.vertices[name] = len(self) + 1  # len(self) + 1 will act as ID for each key
            self.matrix = [[-1] * len(self) for i in range(len(self))]
            return {"status": "success"}
        else:
            return {"status": "Error, node already exists"}

    def add_connection(self, r1, r2, dist=0):
        if r1 and r2 in self.vertices.keys():
            r1 = self.vertices[r1] - 1
            r2 = self.vertices[r2] - 1
            if self.matrix[r1][r2] <= 0:
                self.matrix[r1][r2] = dist
                self.matrix[r2][r1] = dist
                return {"status": "success"}
            else:
                self.matrix[r1][r2] = dist
                self.matrix[r2][r1] = dist
                return {"status": "updated"}
        else:
            return {"status": "Error, router does not exist"}

    def remove_router(self, name):
        try:
            x = 1
            mx_index = self.vertices[name] - 1
            del self.vertices[name]
            for key in self.vertices.keys():
                self.vertices[key] = x
                x = x + 1
            y = len(self.matrix)
            for i in range(y):
                del self.matrix[i][mx_index]
            del self.matrix[mx_index]
            return {"status": "success"}
        except KeyError:
            return

    def remove_connection(self, r1, r2):
        return


rgraph = RouterGraph()


@app.get("/")
def home():
    return {"Data": "Home"}


@app.post("/addrouter")
def addrouter(r: Router):
    router = r.name
    return rgraph.add_router(router)


@app.post("/connect")
def connect(r: RouterConnection):
    r1, r2, dist = r.routerFrom, r.routerTo, int(r.routerDist)
    return rgraph.add_connection(r1, r2, dist)


@app.post("/removerouter")
def removerouter(r: Router):
    router = r.name
    return rgraph.remove_router(router)


@app.post("/removeconnection")
def removeconnection(r: RouterConnection):
    r1, r2 = r.routerFrom, r.routerTo
    return rgraph.remove_connection(r1, r2)

# rgraph.add_router("A")
# rgraph.add_router("B")
# rgraph.add_router("C")
# rgraph.add_router("D")
# rgraph.add_router("A")

# rgraph.print_matrix()
