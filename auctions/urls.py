from django.urls import path
from .views import (
    index,
    create_listing,
    listing_detail,
    watchlist,
    add_to_watchlist,
    category_list,
    category_detail,
    bid,
    close_listing,
    add_comment,
    login_view,
    logout_view,
    register,
)

urlpatterns = [
    path('', index, name='index'),
    path('create_listing/', create_listing, name='create_listing'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('categories/', category_list, name='category_list'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('add_to_watchlist/<int:listing_id>/', add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', watchlist, name='watchlist'),
    path('add_comment/<int:listing_id>/', add_comment, name='add_comment'),
    path('close_listing/<int:listing_id>/', close_listing, name='close_listing'),
    path('listing/<int:listing_id>/', listing_detail, name='listing_detail'),  # Moved to the end
    path('listing/<int:listing_id>/bid/', bid, name='bid'),
    path('bid/<int:listing_id>/', bid, name='bid'),
]


# urlpatterns = [
#     path('', index, name='index'),
#     path('create_listing/', create_listing, name='create_listing'),
#     path('listing/<int:listing_id>/', listing_detail, name='listing_detail'),
#     path('login/', login_view, name='login'),
#     path('logout/', logout_view, name='logout'),
#     path('register/', register, name='register'),
#     path('categories/', category_list, name='category_list'),
#     path('category/<int:category_id>/', category_detail, name='category_detail'),
#     path('listing/<int:listing_id>/', listing_detail, name='listing_detail'),
#     path('add_to_watchlist/<int:listing_id>/', add_to_watchlist, name='add_to_watchlist'),
#     # path('remove_from_watchlist/<int:listing_id>/', remove_from_watchlist, name='remove_from_watchlist'),
#     path('watchlist/', watchlist, name='watchlist'),
#     path('add_comment/<int:listing_id>/', add_comment, name='add_comment'),
#     path('place_bid/<int:listing_id>/', place_bid, name='place_bid'),
#     # path('bid/<int:listing_id>/', place_bid, name='bid'),
#     path('close_listing/<int:listing_id>/', close_listing, name='close_listing'),
# ]
