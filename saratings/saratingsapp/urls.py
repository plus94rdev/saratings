from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from saratingsapp.views import *
from django.conf import settings

"""
New URLS added in Dev
Added new views in Dev for report purchase and subscription:
ie research_reports_subscription_list 
"""

urlpatterns = [
    path("register/", registration, name="register"),
    path("login/", user_login, name="login"),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path("logout/", user_logout, name="logout"),
    path("", sar_home, name="sar_home"),
    path("about/", sar_about, name="sar_about"),
    path("mission-vision/", sar_mission, name="sar_mission"),
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
    path('research-reports/',resarch_publication_list, name="researchPublications"),
    path('list-economic-nuggets/',nuggets_publication_list, name="nuggets_publication_list"),
    path('read-economic-nugget/<str:unique_id>',read_nugget, name="read_nugget"),
    path('list-year-in-review/',year_in_review_publication_list, name="year_in_review_publication_list"),
    path('purchase-research/',purchase_research, name="purchase_research"),
    path('reports-subscriptions/',research_reports_subscription_list, name="reports_subscription_list"),
    path('sar-policies',sar_policy_list,name="SARPoliyList"),
    path('sector-commentary',sector_commentary_list,name="sectorCommentaryList"),
    path('issuer-commentary',issuer_commentary_list,name="issuerCommentaryList"),
    path('annual-reports',annual_reports_list,name="annualReportsList"),
    
     

]

#Append 'MEDIA_URL' and 'MEDIA_ROOT' to urlpatterns for PROD
if IS_PROD:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
