from datetime import datetime
import httplib, urllib
from threading import Thread

from django.db.models.signals import post_save

from resources.models import Resource
from sms_notifications.models import SmsNotification

def notify(resource):
    """
        send sms alerts to the authorised personnel 
        depends on the notification table.
    """
    # get facility for the resource and find the authorised personnel
    fac = resource.facility
    reporters = SmsNotification.objects.get(facility = fac).authorised_personnel
    if rep != Null:
        # constract a msg
        msg = 'From %s' % (fac)
        msg += '%s is now %s' % (resource.name, resource.status)
        msg += 'please check it out.'
        
        # send sms using threads
        for reporter in reporters:
            thread = Thread(target=_send_sms,args=(reporter.id, msg ))
            thread.start()

    return 1

def _send_sms(reporter_id, message_text):
    data = {"uid": reporter_id,
            "text": message_text
            }
    encoded = urllib.urlencode(data)
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    try:
        conn = httplib.HTTPConnection("localhost:8000") # TODO: DON'T HARD CODE THIS!
        conn.request("POST", "/ajax/messaging/send_message", encoded, headers)
        response = conn.getresponse()
    except Exception, e:
        # TODO: better error reporting
        raise
    
# Register to receive signals each time a notify is save/updated
post_save.connect(notify, sender=Resource)

