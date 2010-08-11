from xformmanager.models import *
from hq.models import *
from graphing.models import *
from receiver.models import *
from reporters.utils import *
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from resources.models import *


styleSheet = getSampleStyleSheet()

def run(response,request):
    samples_to_export = request.POST.getlist('samples')
    samples = Resource.objects.filter(id__in = samples_to_export
                                    )
    std = request.POST.get('start_date').split('-')
    ste = request.POST.get('end_date').split('-')
    styear = int(std[0])
    stmonth = int(std[1])
    stday = int(std[2])
    endyear = int(ste[0])
    endmonth = int(ste[1])
    endday = int(ste[2])
    doc = SimpleDocTemplate(response, pagesize=(8.5*inch, 11*inch),)
    lst = []
    

    styNormal = styleSheet['Normal']
    styBackground = ParagraphStyle('background', parent=styNormal)
    styH1 = styleSheet['title']
    month_names = ['0','jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    head = "CommTrack Report"
    head2 = "Date Range : %s-%s-%s to %s-%s-%s" % (styear,month_names[stmonth],stday,endyear,month_names[endmonth],endday)
    lst.append(Paragraph(head, styH1))
    lst.append(Paragraph(' ', styH1))
    lst.append(Paragraph(head2, styNormal))
    lst.append(Paragraph(' ', styH1))

    ts1 = TableStyle([
                ('ALIGN', (0,0), (-1,0), 'RIGHT'),
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ])
    pdf = []
    title = [Paragraph('Domain', styBackground), Paragraph('Facility', styBackground), Paragraph('Name', styBackground),Paragraph('Date', styBackground),Paragraph('Code', styBackground),Paragraph('Status', styBackground)]
    pdf.append(title)
    month_names = ['0','jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for sample in samples:
        domain = '%s'%sample.facility.domain
        facility = '%s'%sample.facility
        name = '%s'%sample.name
        month_name = month_names[sample.date_added.month]
        date = '%s-%s-%s' % ( sample.date_added.day,month_name , sample.date_added.year)
        code = '%s'% sample.code
        status = '%s'%sample.status
        data = [Paragraph(domain, styBackground),Paragraph(facility , styBackground),Paragraph(name, styBackground),Paragraph(date, styBackground),Paragraph(code, styBackground),Paragraph(status, styBackground)]
        pdf.append(data)
    t1 = Table(
    pdf
        )
    t1.setStyle(ts1)
    lst.append(t1)
    lst.append(Spacer(0,10))

    doc.build(lst)

