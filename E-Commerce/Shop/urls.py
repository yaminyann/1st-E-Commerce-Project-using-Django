from django.urls import path
from Shop import views
from django.conf import settings
from django.conf.urls.static import static
from . forms import Login, PasswordChange,PasswordReset, PasswordResetForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>/', views.ProductDetails.as_view(), name='product-detail'),
    path('search/',views.Search, name='search'),
    #cart
    path('buy/', views.buy_now, name='buy-now'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('mycart/',views.Show_my_cart, name='my_cart'),
    path('pluscart/',views.incrase_quantity),
    path('minuscart/',views.decrase_quantity),
    path('removecart/',views.Remove_cart, name='remove'),
    # order page
    path('checkout/', views.checkout, name='checkout'),
    path('order-status/',views.Order_status, name='order_status'),
    path('orders/', views.orders, name='orders'),
    # product
    path('lehenga/', views.lehenga, name='lehenga'),
    path('lehenga/<slug:data>', views.lehenga, name='lehenga_item'),
    path('saree/', views.Saree, name='saree'),
    path('saree/<slug:data>', views.Saree, name='saree_item'),
    # user profile
    path('accounts/login/', auth_views.LoginView.as_view(template_name='Shop/login.html',authentication_form=Login), name='login'),
    path('registration/', views.CustomarRegistrationView.as_view(), name='customerregistration'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.CustomarProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    # change pass
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='Shop/changepassword.html',form_class=PasswordChange, success_url='/password_change_success/'), name='changepassword'),
    path('password_change_success/',auth_views.PasswordChangeView.as_view(template_name='Shop/passChangeSuccess.html'),name='ChangePassDone'),
    # password reset
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='Shop/reset_pass.html',form_class=PasswordReset), name='password_reset'),  
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='Shop/done_reset_pass.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Shop/confirm_pass.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='Shop/reset_complete.html'),name='password_reset_complete'),
    
] + static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)