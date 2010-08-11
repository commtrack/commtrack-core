from rapidsms.webui.utils import render_to_response, paginated
from xformmanager.models import *
from hq.models import *
from graphing.models import *
from receiver.models import *
from domain.decorators import login_and_domain_required
from reporters.utils import *
from reporters.models import Reporter
from facilities.models import Facility
from locations.models import *
from resources.models import *
import csv
from django.http import HttpResponse
import create_pdf
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
from datetime import datetime
#from reportlab import *

logger_set = False

@login_and_domain_required
def reports(request):
    all_samples = Resource.objects.all()
    samples =[]
    for sample in all_samples:
        if sample.facility.domain not in samples:
            samples.append(sample.facility.domain)
    wqmarea = 1
    template_name="reports.html"
    context = {}
    context = {
    "wqmarea":wqmarea,
    "samples":samples,
    "allwqmarea":wqmarea
    }


    return render_to_response(request, template_name,context)

@login_and_domain_required
def sampling_points(request):
    selected_points = request.POST.getlist('area')
    samplez = []
    sample_ids=[]
    all_samples = Resource.objects.filter(facility__domain__in= selected_points)
    for sample in all_samples:
        if sample.facility not in samplez:
            samplez.append(sample.facility)
    for sample_id in all_samples:
        sample_ids.append(sample_id.id)
    template_name="reports.html"
    context = {}
    context = {
    "sampling_points":sampling_points,
    "samples":samplez,
    "selected_wqmarea":sample_ids
    }


    return render_to_response(request, template_name,context)

#ths z status
@login_and_domain_required
def testers(request):
    selected_wqma = request.POST.getlist('selected_wqm')
    selected_samplingPoints = request.POST.getlist('sampling_points')
    samples = Resource.objects.filter(id__in = selected_wqma,
                                    facility__in = selected_samplingPoints,
                                    )

    samples_ids=[]
    testers=[]
    for sample in samples:
        samples_ids.append(sample.id)
        if sample.status not in testers:
            testers.append(sample.status)
    template_name="reports.html"
    context = {}
    context = {
    "testers":testers,
    "selected_wqma":selected_wqma,
    "samples_ids":samples_ids,
    }


    return render_to_response(request, template_name,context)

def date_range(request):
    selected_testers = request.POST.getlist('testers')
    selected_wqm_samplingPoints = request.POST.getlist('selected_testers')
    samples = Resource.objects.filter(id__in = selected_wqm_samplingPoints,
                                    status__in = selected_testers,
                                    
                                    )
    samples_ids=[]
    for sample in samples:
        samples_ids.append(sample.id)
    daterange = 1
    end_date = datetime.today()
    month_names = ['0','jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    start_date = datetime(end_date.year-1,end_date.month,end_date.day)
    month_name = month_names[end_date.month]
    template_name="reports.html"
    context = {}
    context = {
    "daterange":daterange,
    "samples":samples,
    "samples_ids":samples_ids,
    "start_date":start_date,
    "end_date":end_date,
    "month_names":month_name

    }


    return render_to_response(request, template_name,context)

def create_report(request):
    selected_wqm_samplingPoints_tester = request.POST.getlist('selected_all')
    selected_start_date = request.POST.getlist('startDate')
    datestart = []
    dateend =[]
    for p in selected_start_date:
        datestart.append(p)
    selected_end_date = request.POST.getlist('endDate')
    for j in selected_end_date:
        dateend.append(j)
    std = datetime(int(datestart[2]),int(datestart[1]),int(datestart[0]))
    ste = datetime(int(dateend[2]),int(dateend[1]),int(dateend[0]))
    samples = Resource.objects.filter(id__in = selected_wqm_samplingPoints_tester,
                                date_added__range = (std,ste)
                                    )
    samples_ids=[]
    for sample in samples:
        samples_ids.append(sample.id)
    data = 1
    template_name="reports.html"

    context = {}
    context = {
        "data":data,
        "selected_start_date":std,
        "selected_end_date":ste,
        "samples_ids":samples_ids,
        "samples":samples
    }


    return render_to_response(request, template_name,context)


@login_and_domain_required
def export_csv(request):
    samples_to_export = request.POST.getlist('samples')
    samples = Resource.objects.filter(id__in = samples_to_export
                                    )
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=CommTrackReport.csv'
    writer = csv.writer(response)

    title = ['Domain', 'Facility', 'Name','Date','Code','Status']
    writer.writerow(title)

    for sample in samples:
        month_names = ['0','jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        month_name = month_names[sample.date_added.month]
        temp = '%s-%s-%s' % ( sample.date_added.day,month_name , sample.date_added.year)
        data = [sample.facility.domain, sample.facility, sample.name,temp,sample.code,sample.status]
        writer.writerow(data)
    return response

@login_and_domain_required
def pdf_view(request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=CommTrackReport.pdf'
    create_pdf.run(response, request)
    return response

