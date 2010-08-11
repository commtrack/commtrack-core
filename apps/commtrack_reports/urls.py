from django.conf.urls.defaults import *

## reports view
urlpatterns = patterns('commtrack_reports.views',
    (r'^commtrackreports$', 'reports'),
    (r'^sampling_points$', 'sampling_points'),
    (r'^commtrack_testers$', 'testers'),
    (r'^date_range$', 'date_range'),
    (r'^create_report$', 'create_report'),
    (r'^export_csv$', 'export_csv'),
    (r'^export_pdf$', 'pdf_view'),
#    (r'^test$', 'test'),

)


