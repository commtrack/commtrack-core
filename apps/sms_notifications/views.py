from domain.decorators import login_and_domain_required
from rapidsms.webui.utils import render_to_response, paginated
from sms_notifications.models import SmsNotification, NotificationChoice
from sms_notifications.forms import SmsNotificationForm 

@login_and_domain_required
def index(request):
    template_name = 'index.html'

    notifications = SmsNotification.objects.all().order_by("-authorised_personnel")

    return render_to_response(request,
                              template_name, 
                              {
                               "notifications": paginated(request, notifications, prefix="smsnotice"),
                               }
                              )

@login_and_domain_required
def add_notifications(request):
    template_name = "sms-notifications.html"
    if request.method == 'POST': # If the form has been submitted...
        form = SmsNotificationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # saving the form data is not cleaned
            form.save()
            return message(request,
                        "SMS Notification Added",
                        link="/smsnotification")
    else:
        form = SmsNotificationForm() # An unbound form

    return render_to_response(request,
                              template_name, 
                              {
                               'form': form,
                               }
                              )

@login_and_domain_required
def edit_notifications(request, pk):
    template_name = "sms-notifications.html"
    notification = get_object_or_404(SmsNotification, pk=pk)
    if request.method == 'POST': # If the form has been submitted...
        form = SmsNotificationForm(request.POST, instance = notification) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # saving the form data is not cleaned
            form.save()
            return message(request,
                        "SMS Notification Updated",
                        link="/smsnotification")
    else:
        form = SmsNotificationForm(instance=notification)
    
    return render_to_response(request,
                              template_name, 
                              {
                               'form': form,
                               'notification': notification,
                               }
                              )

@login_and_domain_required
def delete_notifications(req, pk):
    notification = get_object_or_404(SmsNotification, pk=pk)
    notification.delete()

    transaction.commit()
    id = int(pk)
    return message(req,
        "SMS Notification %d deleted" % (id),
        link="/smsnotification")
