from django.contrib import admin
from .models import ProductCU
from .models import ProductEmart24
from .models import ProductGS25
from .models import ProductSevenvEleven
from .models import ProductMiniStop
from .models import Post

admin.site.register(Post)
admin.site.register(ProductCU)
admin.site.register(ProductEmart24)
admin.site.register(ProductGS25)
admin.site.register(ProductSevenvEleven)
admin.site.register(ProductMiniStop)

