from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),

    path('useraccounts/', views.UserAccountViewSet.as_view({'get': 'list', 'post': 'create'}), name='useraccount-list'),
    path('useraccounts/<int:pk>/', views.UserAccountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='useraccount-detail'),

    path('analysts/', views.AnalystViewSet.as_view({'get': 'list', 'post': 'create'}), name='analyst-list'),
    path('analysts/<int:pk>/', views.AnalystViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='analyst-detail'),

    path('administrators/', views.AdministratorViewSet.as_view({'get': 'list', 'post': 'create'}), name='administrator-list'),
    path('administrators/<int:pk>/', views.AdministratorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='administrator-detail'),

    path('sops/', views.SOPViewSet.as_view({'get': 'list', 'post': 'create'}), name='sop-list'),
    path('sops/<int:pk>/', views.SOPViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='sop-detail'),

    path('usersopactions/', views.UserSOPActionViewSet.as_view({'get': 'list', 'post': 'create'}), name='usersopaction-list'),
    path('usersopactions/<int:pk>/', views.UserSOPActionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='usersopaction-detail'),

    path('clients/', views.ClientViewSet.as_view({'get': 'list', 'post': 'create'}), name='client-list'),
    path('clients/<int:pk>/', views.ClientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='client-detail'),

    path('warehouses/', views.WarehouseViewSet.as_view({'get': 'list', 'post': 'create'}), name='warehouse-list'),
    path('warehouses/<int:pk>/', views.WarehouseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='warehouse-detail'),

    path('warehouseclientlinks/', views.WarehouseClientLinkViewSet.as_view({'get': 'list', 'post': 'create'}), name='warehouseclientlink-list'),
    path('warehouseclientlinks/<int:pk>/', views.WarehouseClientLinkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='warehouseclientlink-detail'),

    path('locations/', views.LocationViewSet.as_view({'get': 'list', 'post': 'create'}), name='location-list'),
    path('locations/<int:pk>/', views.LocationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='location-detail'),

    path('equipment/', views.EquipmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='equipment-list'),
    path('equipment/<int:pk>/', views.EquipmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='equipment-detail'),

    path('maintenancelogs/', views.MaintenanceLogViewSet.as_view({'get': 'list', 'post': 'create'}), name='maintenancelog-list'),
    path('maintenancelogs/<int:pk>/', views.MaintenanceLogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='maintenancelog-detail'),

    path('samples/', views.SampleViewSet.as_view({'get': 'list', 'post': 'create'}), name='sample-list'),
    path('samples/<int:pk>/', views.SampleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='sample-detail'),

    path('inprocess/', views.InProcessViewSet.as_view({'get': 'list', 'post': 'create'}), name='inprocess-list'),
    path('inprocess/<int:pk>/', views.InProcessViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='inprocess-detail'),

    path('stability/', views.StabilityViewSet.as_view({'get': 'list', 'post': 'create'}), name='stability-list'),
    path('stability/<int:pk>/', views.StabilityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='stability-detail'),

    path('finishedproducts/', views.FinishedProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='finishedproduct-list'),
    path('finishedproducts/<int:pk>/', views.FinishedProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='finishedproduct-detail'),

    path('usersampleactions/', views.UserSampleActionViewSet.as_view({'get': 'list', 'post': 'create'}), name='usersampleaction-list'),
    path('usersampleactions/<int:pk>/', views.UserSampleActionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='usersampleaction-detail'),

    path('tests/', views.TestViewSet.as_view({'get': 'list', 'post': 'create'}), name='test-list'),
    path('tests/<int:pk>/', views.TestViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='test-detail'),

    path('sampletestlinks/', views.SampleTestLinkViewSet.as_view({'get': 'list', 'post': 'create'}), name='sampletestlink-list'),
    path('sampletestlinks/<int:pk>/', views.SampleTestLinkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='sampletestlink-detail'),

    path('testequipmentlinks/', views.TestEquipmentLinkViewSet.as_view({'get': 'list', 'post': 'create'}), name='testequipmentlink-list'),
    path('testequipmentlinks/<int:pk>/', views.TestEquipmentLinkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='testequipmentlink-detail'),

    path('reagents/', views.ReagentViewSet.as_view({'get': 'list', 'post': 'create'}), name='reagent-list'),
    path('reagents/<int:pk>/', views.ReagentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='reagent-detail'),

    path('userreagentactions/', views.UserReagentActionViewSet.as_view({'get': 'list', 'post': 'create'}), name='userreagentaction-list'),
    path('userreagentactions/<int:pk>/', views.UserReagentActionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='userreagentaction-detail'),

    path('testreagentlinks/', views.TestReagentLinkViewSet.as_view({'get': 'list', 'post': 'create'}), name='testreagentlink-list'),
    path('testreagentlinks/<int:pk>/', views.TestReagentLinkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='testreagentlink-detail'),

    path('versionchanges/', views.VersionChangeViewSet.as_view({'get': 'list', 'post': 'create'}), name='versionchange-list'),
    path('versionchanges/<int:pk>/', views.VersionChangeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='versionchange-detail'),

    path('register/', views.UserRegistrationView.as_view(), name='register'),
]
