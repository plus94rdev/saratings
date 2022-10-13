from django.urls import path
from django.conf.urls.static import static
from saratingsapp.views import *
from django.conf import settings


urlpatterns = [
    
    path("", sar_home, name="sar_home"),
    path("about/", sar_about, name="sar_about"),
    path("team/", sar_team, name="sar_team"),
    path("contact/", sar_contact, name="sar_contact"),
    path('events/',event_homepage, name="eventsHomepage"),
    path('event-rsvp/<str:event_id>',event_rsvp, name="eventRSVP"),
    path('media-page/',media_homepage, name="mediaHomepage"),
    path('regulatory/public-commentary/articles',public_commentary_article_list, name="publicCommentaryArticleList"),
    path('regulatory/public-commentary/article/<str:unique_id>',view_commentary_article, name="viewCommentaryArticle"),
    path('regulatory/public-commentary/article/<str:unique_id>/comment',comment_commentary_article, name="commentCommentaryArticle"),
    path('ratings-publication/',ratings_publication_list, name="ratingsPublications"),
    path('ratings-methodology/',ratings_methodology_list, name="ratingsMethodologies"),
]

#Append 'MEDIA_URL' and 'MEDIA_ROOT' to urlpatterns for PROD
if IS_PROD:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
