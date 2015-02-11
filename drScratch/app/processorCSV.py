#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from django.http import HttpResponse

def fistCSV():
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="firstDr.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Paco', '657483922', 'Madrid'])
    writer.writerow(['Second row', 'Lucia', '657390033', 'Quito'])

    return response
