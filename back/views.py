from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Vulnerability, Date
from django.db import connection
from django.db.models import Count
import json
from django.core import serializers


@login_required(login_url='/account/login/')
def fake(request):
    return redirect("back:dashboard")

@login_required(login_url='/account/login/')
def dash(request):
    '''
     How many vulnerabilities are critical, high, medium
     
    '''
    
    ## RAW SQL
    #cursor = connection.cursor()
    # cursor.execute('''SELECT COUNT(vul_name), severity FROM vulnerabilities GROUP BY severity''')
    # rom = cursor.fetchall() #list of tuples
    # rs = json.dumps(dict(rom))
    # print(rs)

    ############################################################################################

    ## Django ORM
    rows = Vulnerability.objects.values('severity').annotate(howmany=Count('vul_name'))
    severity = list()
    howmany = list()
    for i in rows:
        severity.append(str(i['severity']))
        howmany.append(str(i['howmany']))
    
    level = json.dumps(severity)
    how = json.dumps(howmany)

    return render(request, "dashboard.html", {"level":level, "how":how})

@login_required(login_url='/account/login/')
def graph2(request):
    '''
      How many vulnerabilities are on each date

    '''
    
    ## RAW SQL
    # cursor = connection.cursor()
    # cursor.execute('''SELECT dates.publish_date, COUNT(dates.vuln_id) FROM dates GROUP BY dates.publish_date''')
    # rom = cursor.fetchall() #list of tuples
    # rom = dict(rom) # this dict contain objects.datetime
    # keys = [str(date_obj) for date_obj in rom.keys()]
    # values = rom.values()
    #rs = json.dumps(rom)

    #########################################################################################
    
    ## Django ORM
    rows = Date.objects.values('publish_date').annotate(howmany=Count('vuln')) #list of dict
    dates = list()
    howmany = list()
    for i in rows:
        dates.append(str(i['publish_date']))
        howmany.append(str(i['howmany']))

    dates = json.dumps(dates) # string
    howmany = json.dumps(howmany) # string
    
    return HttpResponse("a")


@login_required(login_url='/account/login/')
def graph3(request):
    '''  
    This Lists all severity="critical" vulnerabilities and their dates using foreign key.
    
    !!!! if using sql raw selecting the foreign key... use (dates.vuln_id) not (dates.vuln) 
    because django add (_id) at the end !!!!

    '''
    
    ## RAW SQL
    # cursor = connection.cursor()
    # rows = cursor.execute('''SELECT vulnerabilities.vul_name, dates.publish_date FROM vulnerabilities JOIN dates on vulnerabilities.id = dates.vuln_id WHERE vulnerabilities.severity="critical"''')
    # rom = cursor.fetchall() #list of tuples
    # rom = dict(rom)
    # keys = list(rom.keys())
    # values = [date_obj.strftime("%d %b %Y") for date_obj in rom.values()]
    
    # strkey = json.dumps(keys)
    # strvalue = json.dumps(values)
    ##################################################################################################
    ## Django ORM
    record = Vulnerability.objects.filter(severity="critical")
    rows = list(Date.objects.filter(vuln__in=record).select_related())
    dates = [str(date_obj) for date_obj in rows]
    print(dates)
    return HttpResponse("Graph3")