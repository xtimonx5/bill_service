from django.urls import path, include

from .views import (
    RegistrationView,
    PurchaseView,
    WithdrawalView,
    AccountView,
)

urlpatterns = [
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # account related
    path('register/', RegistrationView.as_view(), name='register'),
    path('account/', AccountView.as_view(), name='account'),

    # balance related
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('withdrawal/', WithdrawalView.as_view(), name='withdrawal'),

]
