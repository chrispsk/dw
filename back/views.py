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
    This Lists all vulnerability levels for each date.... using foreign key.
    
    !!!! if using sql raw selecting the foreign key... use (dates.vuln_id) not (dates.vuln) 
    because django add (_id) at the end !!!!

    '''
    
    ## RAW SQL
    cursor = connection.cursor()

    cursor.execute('''SELECT dates.publish_date, vulnerabilities.severity FROM vulnerabilities 
    JOIN dates on vulnerabilities.id = dates.vuln_id 
    ''')
    
    rom = cursor.fetchall() #list of tuples
    asd = dict()
    for d in rom:
        a = str(d[0]) # grab each data
        b = d[1]
        if a not in asd:
            asd[a] = []
            asd[a].append(b)
        else:
            asd[a].append(b)
    print(asd)
    keys = list(asd.keys())
    values = list(asd.values())
    lows = []
    mediums = []
    highs = []
    criticals = []
    for z in values:
        low = z.count('low')
        medium = z.count('medium')
        high = z.count('high')
        critical = z.count('critical')
        lows.append(low)
        mediums.append(medium)
        highs.append(high)
        criticals.append(critical)
    print(keys)
    print(lows)
    print(criticals)
    
    dat = json.dumps(keys)
    lo = json.dumps(lows)
    me = json.dumps(mediums)
    hi = json.dumps(highs)
    cri = json.dumps(criticals)
    
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
    rows = Date.objects.values('publish_date').annotate(howmany=Count('vuln')) #list of dict
    ok = list()
    for i in rows:
        ok.append([str(i['publish_date']), i['howmany']])
    
    # dates = list()
    # howmany = list()
    # for i in rows:
    #     dates.append(str(i['publish_date']))
    #     howmany.append(str(i['howmany']))

    dates = json.dumps(ok) # string
    # howmany = json.dumps(howmany) # string
    return render(request, "graph3.html", {"da":dates})
    # return render(request, "graph3.html", {"dat": dates, "how": howmany})

    