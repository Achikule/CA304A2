#!usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
description = """
This script requires the following modules to run: Pydantic, typing and FastAPI
"""


tags_metadata = [
    {
        "name": "addrouter",
        "description": """This endpoint instantiates a RouterGraph object and adds a router from input as one of 
        the vertices in an undirected graph. Each vertex is given an ID based on the order they were added. 
        An (n x n) adjacency matrix is initialized where n is the number of the number of vertices. 
        If successfully created, this message will be returned: {"status": "success"}. 
        If the router already exists, this message will be returned: {"status": "Error, node already exists"}""",
    },
    {
        "name": "connect",
        "description": """This endpoint takes in two routers to connect and the weight/distance of that connection.
        This weight is updated on the adjacency matrix. If the input is a new connection definition, this message is
        returned: {"status": "success"}. If the connection between the 2 routers was defined before and the function is 
        called again, the weight will be updated and this message is returned: {"status": "updated"}. If one or more
        of the routers don't exist, this message is returned: {"status": "Error, router does not exist"}
        """


    },
    {
        "name": "removerouter",
        "description": """This endpoint removes the router given to it. First, the router is removed from vertices and
        the IDs of all vertices are updated to reflect this. Next, the row and column of this router is removed from the
        matrix, removing all pre-existing connections to other routers. If this process is successful, this message
        is returned {"status": "success"}""",
    },
    {
        "name": "removeconnection",
        "description": """This endpoint removes a connection between any two routers that exist in vertices. This is 
        achieved by setting the values in the adjacency matrix where they connect back to -1. If successful, 
        {"status": "success"} is returned.""",
    }
]

app = FastAPI(title="Alen Joy CA304 Assessment 2",
              description=description,
              openapi_tags=tags_metadata)


class Router(BaseModel):
    name: str


class RouterConnection(BaseModel):
    routerFrom: str
    routerTo: str
    routerDist: Optional[int]


class RouterGraph:
    """ An undirected weighted graph created using an adjacency matrix"""
    def __init__(self):
        self.vertices = {}
        self.matrix = []
        self.visited = []

    def __len__(self):
        return len(self.vertices.keys())

    def print_matrix(self):
        return self.matrix

    def add_router(self, name):
        if name not in self.vertices.keys():
            self.vertices[name] = len(self) + 1  # len(self) + 1 will act as an ID for each key & len -1 will be index
            self.matrix = [[-1] * len(self) for i in range(len(self))]                    # in the adjacency matrix
            return {"status": "success"}
        else:
            return {"status": "Error, node already exists"}

    def add_connection(self, r1, r2, dist=0):
        try:
            if r1 and r2 in self.vertices.keys():
                r1 = self.vertices[r1] - 1  # ID value is always 1 more than matrix index
                r2 = self.vertices[r2] - 1
                if self.matrix[r1][r2] <= 0:  # set distance in adjacency matrix
                    self.matrix[r1][r2] = dist
                    self.matrix[r2][r1] = dist
                    return {"status": "success"}
                else:
                    self.matrix[r1][r2] = dist
                    self.matrix[r2][r1] = dist
                    return {"status": "updated"}
            else:
                return {"status": "Error, router does not exist"}

        except KeyError:
            return {"status": "Error, router does not exist"}

    def remove_router(self, name):
        try:
            x = 1
            mx_index = self.vertices[name] - 1
            del self.vertices[name]
            for key in self.vertices.keys():  # reset and re-order ID in dictionary
                self.vertices[key] = x
                x = x + 1
            y = len(self.matrix)
            for i in range(y):  # remove row and column of router in question from matrix
                del self.matrix[i][mx_index]
            del self.matrix[mx_index]
            return {"status": "success"}
        except KeyError:
            return

    def remove_connection(self, r1, r2):
        try:
            if r1 and r2 in self.vertices.keys():  # reset removed connections in matrix
                r1 = self.vertices[r1] - 1
                r2 = self.vertices[r2] - 1
                self.matrix[r1][r2] = -1
                self.matrix[r2][r1] = -1
                return {"status": "success"}
            elif r1 or r2 not in self.vertices.keys():
                return
        except KeyError:
            return

    def route(self, r1, r2):

        return 0


rgraph = RouterGraph()


@app.get("/")
def home():
    return {"Data": "Home"}


@app.post("/addrouter", tags=["addrouter"])
def addrouter(r: Router):
    router = r.name
    return rgraph.add_router(router)


@app.post("/connect", tags=["connect"])
def connect(r: RouterConnection):
    r1, r2, dist = r.routerFrom, r.routerTo, int(r.routerDist)
    return rgraph.add_connection(r1, r2, dist)


@app.post("/removerouter", tags=["removerouter"])
def removerouter(r: Router):
    router = r.name
    return rgraph.remove_router(router)


@app.post("/removeconnection", tags=["removeconnection"])
def removeconnection(r: RouterConnection):
    r1, r2 = r.routerFrom, r.routerTo
    return rgraph.remove_connection(r1, r2)


@app.post("/route", tags=["route"])
def route(r: RouterConnection):
    r1, r2 = r.routerFrom, r.routerTo
    return rgraph.route(r1, r2)

