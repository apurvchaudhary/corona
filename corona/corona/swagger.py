from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# swagger method
schema_view = get_schema_view(
    openapi.Info(
        title="Corona Statistics API Docs",
        default_version='Version 1.0',
        description="https://www.apurvchaudhary.site/corona/home API swagger",
        license=openapi.License(name="Self Signed License © apurvchaudhary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)