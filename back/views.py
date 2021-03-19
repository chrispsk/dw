from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Vulnerability, Date
from django.db import connection
from django.db.models import Count
import json
from django.core import serializers


@login_required(login_url='/account/login/')
def dash(request):
    #!!!! if using sql raw use dates.vuln_id not dates.vuln because django add _id at the end of the foreign key
    cursor = connection.cursor()
    
    ######### How many vulnerabilities are critical, high, medium ###########
    ## RAW SQL
    # cursor.execute('''SELECT COUNT(vul_name), severity FROM vulnerabilities GROUP BY severity''')
    
    ## Django ORM
    rows = list(Vulnerability.objects.values('severity').annotate(howmany=Count('vul_name')))    
    r = json.dumps(rows) # string
    
    #loaded_r = json.loads(r)
    ########## How many vulnerabilities are on each date ############
    ## RAW SQL
    #rows = cursor.execute('''SELECT COUNT(dates.vuln_id), dates.publish_date FROM dates GROUP BY dates.publish_date''')
    ## Django ORM
    #rows = Date.objects.values('publish_date').annotate(howmany=Count('vuln'))

    ######### List all critical vulnerabilities and the dates
    ## RAW SQL
    #rows = cursor.execute('''SELECT vulnerabilities.vul_name, dates.publish_date FROM vulnerabilities FULL OUTER JOIN dates on vulnerabilities.id = dates.vuln_id WHERE vulnerabilities.severity="critical"''')
    
    ## Django ORM
    # record = Vulnerability.objects.filter(severity="critical")
    # rows = Date.objects.filter(vuln__in=record).select_related()
    
    # rom = cursor.fetchall() #list of tuples
    # rs = json.dumps(dict(rom))
    # print(rs)

    #return HttpResponse(rows)
    return render(request, "dashboard.html", {"rows":r})

def graph2(request):

    return HttpResponse("Graph2")

def graph3(request):

    return HttpResponse("Graph3")