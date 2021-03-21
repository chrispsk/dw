from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Vulnerability, Date
from django.db import connection
from django.db.models import Count
import json
from django.core import serializers
from collections import Counter


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
    
    # Highcharts. The choosen Graph need separated lists
    severity = list()
    howmany = list()
    for i in rows:
        severity.append(str(i['severity']))
        howmany.append(str(i['howmany']))
    
    # Converting into json
    level = json.dumps(severity)
    how = json.dumps(howmany)

    return render(request, "dashboard.html", {"level":level, "how":how})


@login_required(login_url='/account/login/')
def graph2(request):
    '''  
    This Lists all vulnerability levels for each date.... using foreign key.
    
    !!!! if using sql raw selecting the foreign key... use (dates.vuln_id) not (dates.vuln) 
    because django add (_id) at the end !!!!

    '''
    cursor = connection.cursor()
    # can use IF function on mysql
    cursor.execute('''
    SELECT dates.publish_date,
    SUM(CASE WHEN vulnerabilities.severity = "critical" THEN 1 ELSE 0 END) as critic,
    SUM(CASE WHEN vulnerabilities.severity = "high" THEN 1 ELSE 0 END) as high,
    SUM(CASE WHEN vulnerabilities.severity = "medium" THEN 1 ELSE 0 END) as medium,
    SUM(CASE WHEN vulnerabilities.severity = "low" THEN 1 ELSE 0 END) as low
    FROM vulnerabilities
    INNER JOIN dates
    ON
    vulnerabilities.id = dates.vuln_id
    GROUP BY
    dates.publish_date
    ''')
    rom = cursor.fetchall() #list of tuples

    # Highcharts. The choosen Graph need separated lists
    dates = list()
    critic = list()
    high = list()
    medium = list()
    low = list()

    # data formating: collecting per category 'ready-made' to pass it easily
    for i in rom:
        dates.append(str(i[0]))
        critic.append(i[1])
        high.append(i[2])
        medium.append(i[3])
        low.append(i[4])

    # converting into json
    dat = json.dumps(dates) # ['a', 'b']
    lo = json.dumps(low) 
    me = json.dumps(medium)
    hi = json.dumps(high)
    cri = json.dumps(critic)

    context = {
        "dat": dat,
        "lo": lo,
        "me": me,
        "hi": hi,
        "cri": cri
    }
    return render(request, "graph2.html", context)


@login_required(login_url='/account/login/')
def graph3(request):
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
    rows = Date.objects.values('publish_date').annotate(howmany=Count('vuln'))
    ok = list()
    for i in rows:
        ok.append([str(i['publish_date']), i['howmany']])
    dates = json.dumps(ok) # string
    return render(request, "graph3.html", {"da":dates})


