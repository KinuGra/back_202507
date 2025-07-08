"""
URL configuration for back_202507 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # Djangoの管理サイト機能を利用するためのモジュールをインポート
from django.urls import path, include # URLパスを定義するためのpath関数と、他のURLconfを参照するためのinclude関数をインポート
from rest_framework.routers import DefaultRouter # DRFから、デフォルトのルータークラスDefaultRouterをインポート。ViewSetとURLの自動マッピングを可能にする
from main.views import ItemViewSet, RoomViewSet # api/views.pyからItemViewSetクラスをインポート

# DefaultRouterのインスタンスを作成
router = DefaultRouter()
# ItemViewSetをitemsパスでルーターに登録している。これにより、ItemViewSetに定義された操作に基づいて、自動的にURLが生成される
router.register(r'items', ItemViewSet)
router.register(r'rooms', RoomViewSet) # 追加


from main.views import UserViewSet # api/views.pyからUserViewSetクラスをインポート

# DefaultRouterのインスタンスを作成
router = DefaultRouter()
# UserViewSetをusersパスでルーターに登録している。これにより、UserViewSetに定義された操作に基づいて、自動的にURLが生成される
router.register(r'users', UserViewSet)

urlpatterns = [
    # Django管理サイトへのpath
    path('admin/', admin.site.urls),
    path('', include('main.urls')),

    # routerで生成されたすべてのURLを/api/パス以下に含めるように定義。
    # これにより、ItemViewSetの操作に対応するURLが/api/items/のようにアクセスできるようにする
    path('api/', include(router.urls))
]
