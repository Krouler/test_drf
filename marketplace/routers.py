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
        routers.Route(url=r'^{prefix}/info$',
                      mapping={'get': 'retrieve'},
                      name='{basename}-info-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'}),
        routers.Route(url=r'^{prefix}/invite_employee$',
                      mapping={'put': 'update', 'patch': 'partial_update'},
                      name='{basename}-einvite-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'}),
        routers.Route(url=r'^{prefix}/change_main_employee$',
                      mapping={'put': 'update', 'patch': 'partial_update'},
                      name='{basename}-meinvite-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'}),
    ]
