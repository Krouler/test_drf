from rest_framework import routers


class ShopRouter(routers.SimpleRouter):

    routes = [
        routers.Route(url=r'^{prefix}$',
                      mapping={'get': 'list', 'post': 'create'},
                      name='{basename}-list',
                      detail=False,
                      initkwargs={'suffix': 'List'}),
        routers.Route(url=r'^{prefix}/{lookup}$',
                      mapping={'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'},
                      name='{basename}-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'}),
    ]


class ConfDataRouter(routers.SimpleRouter):
    routes = [
        routers.Route(url=r'^{prefix}$',
                      mapping={'put': 'update', 'patch': 'partial_update'},
                      name='{basename}-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'}),
    ]
