from django.db import models

class Vulnerability(models.Model): # USER
    vul_name = models.CharField(max_length=200)
    summary = models.TextField()
    severity = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'vulnerabilities'

    def __str__(self):
        return self.vul_name

class Date(models.Model): # CAR
    vuln = models.ForeignKey(Vulnerability, on_delete=models.CASCADE) #in case you delete a vulnerability what will happen with his Details?
    publish_date = models.DateField()

    class Meta:
        db_table = 'dates'

    def __str__(self):
        return str(self.publish_date)

 