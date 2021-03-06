"""urls config for finance at harshp_com"""

from django.conf.urls import include, url

from . import views

finance_urlspatterns = [
    # homepage
    url(r'^$', views.home, name='home'),
    url(r'^logout/$', views.logout_user, name='logout'),
    # accounts
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accounts/(?P<slug>[\w-]+)/$', views.account, name='account'),
    # spending by month
    url(
        r'^monthly-spendings/$',
        views.monthly_spendings_list, name='monthly-spendings-list'),
    url(
        r'^monthly-spendings/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.monthly_spendings, name='monthly-spendings'),
    # categories
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/(?P<slug>[\w-]+)/$', views.category, name='category'),
    # tags
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^tags/(?P<slug>[\w-]+)/$', views.tag, name='tag'),
    # budgets
    url(r'^budgets/$', views.budgets, name='budgets'),
    url(r'^budgets/(?P<pk>[0-9]+)/$', views.budget, name='budget'),
    # transactions
    url(r'^transactions/$', views.transactions, name='transactions'),
    url(
        r'^transactions/planned/$',
        views.planned_transactions, name='planned_transactions'),
    url(r'^transactions/transfers$', views.transfers, name='transfers'),
    url(
        r'^transactions/(?P<pk>[0-9]+)/$',
        views.transaction, name='transaction'),
    url(
        r'^transactions/planned/(?P<pk>[0-9]+)/$',
        views.planned_transaction, name='planned_transaction'),
    url(
        r'^transactions/transfers/(?P<pk>[0-9]+)/$',
        views.transfer, name='transfer'),
    # reports
]

urlpatterns = [
    url(r'', include(finance_urlspatterns, namespace='finance')),
]

handler404 = 'harshp_com.views.handler404'
