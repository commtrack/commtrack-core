import re
from datetime import datetime

import rapidsms
from models import Resource, ResourceSupplyRequest 
from reporters.models import Reporter

class App (rapidsms.app.App):
    #   Matches the sms pattern for resource request and
    #   update status features.
    #   pattern: resource request resource_code remarks
    #   pattern: resource update resource_code curr_status

    pattern = re.compile(r'^resource\s+(request|update)\s+([a-zA-Z0-9_]*)\s+(\w*)',re.IGNORECASE)
    #pattern = re.compile(r'^resource',re.IGNORECASE)
    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        """Parse and annotate messages in the parse phase."""
        pass

    def handle (self, message):
        """Add your main application logic in the handle phase."""
        response = self.pattern.findall(message.text)
        print "***********************"
        if response:
            entry = response[0]
            entry_time = datetime.now()
#            reporter = message.connection.identity
            reporter = Reporter.objects.get(id=1)
            resource_code = entry[1]
#            extra_info = entry[2]

            if entry[0].lower() == "request":
                resource_code = entry[1];
                remarks = entry[2];
                this_resource = Resource.objects.get(code = resource_code)
                if this_resource: 
                    request = ResourceSupplyRequest()
                    request.user = reporter
                    request.request_date = entry_time
                    request.request_remarks = remarks
                    request.status = 'pending'
                    request.resource = this_resource
                    # saving the request
                    request.save()
                    # Everthing went well.  Generate a response
                    message.respond("Your resource request is in progress")
                else:
                    message.respond("Unable to process your request")
#                message.respond("Your resource request is in progress")

            if entry[0].lower() == "update":
                this_resource = Resource.objects.get(code = resource_code)
#             Generate a response
                message.respond("Resource status is updated!")

            # TODO: Generate a general error reporting

    def cleanup (self, message):
        """Perform any clean up after all handlers have run in the
           cleanup phase."""
        pass

    def outgoing (self, message):
        """Handle outgoing message notifications."""
        pass

    def stop (self):
        """Perform global app cleanup when the application is stopped."""
        pass
