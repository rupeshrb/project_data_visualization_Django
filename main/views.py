from django.shortcuts import render
from django.db import models
from .models import InternData  # Import your model
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import plotly.graph_objects as go  # Use plotly.graph_objects for more customization
import plotly.offline as opy
import json
import plotly.express as px
import pandas as pd 

def index(request):
    # Get the count of total entries from the MySQL database
    total_entries_count = InternData.objects.count()

    # Fetch the data you want to display in the chart
    data = list(InternData.objects.values('start_year', 'sector','intensity'))
    region_data = InternData.objects.values('region').annotate(data_count=models.Count('id'))

    # Prepare the data for the pie chart
    labels = [entry['region'] for entry in region_data]
    data_counts = [entry['data_count'] for entry in region_data]
    
    data1 = InternData.objects.all().order_by('end_year')
    
    # Extract the 'start_year' and 'intensity' values from the data
    end_years = [entry.end_year for entry in data1]
    intensities = [entry.intensity for entry in data1]

    # Create the line chart
    plt.figure(figsize=(10, 6))
    plt.plot(end_years, intensities, marker='o')
    plt.xlabel('end Year')
    plt.ylabel('Intensity')
    plt.title('Line Chart of Intensity Over Time')

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the chart as a base64 string for embedding in HTML
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    context = {
        'total_entries_count': total_entries_count,
        'intensity_data_json': json.dumps(data),  # Convert data to JSON
        'labels': labels,
        'data_counts': data_counts,
        'chart_data': chart_data,
    }

    return render(request, 'index.html', context)


def filter_form1(request):
    end_year = request.GET.get('filter-end-year')
    intensity = request.GET.get('filter-intensity')

    # Query the database based on filters for Form 1
    queryset = InternData.objects.all()  # Replace 'YourModel' with your actual model name

    if end_year:
        queryset = queryset.filter(end_year=end_year)

    if intensity:
        queryset = queryset.filter(intensity=intensity)

    # Extract the data from the queryset
    end_years = [item.end_year for item in queryset]
    intensities = [item.intensity for item in queryset]

    # Create a scatter plot for Form 1
    fig = go.Figure(data=go.Scatter(x=end_years, y=intensities, mode='markers'))
    fig.update_layout(title='Intensity vs. End Year ')

    # Convert the chart to HTML for Form 1
    chart_html = opy.plot(fig, auto_open=False, output_type='div')

    return chart_html


def filter_form2(request):
    start_year = request.GET.get('filter-start-year2')
    intensity2 = request.GET.get('filter-intensity2')

    # Query the database based on filters for Form 2
    queryset = InternData.objects.all()  # Replace 'YourModel' with your actual model name

    if start_year:
        queryset = queryset.filter(start_year=start_year)

    if intensity2:
        queryset = queryset.filter(intensity=intensity2)

    # Extract the data from the queryset
    start_years = [item.start_year for item in queryset]
    intensities = [item.intensity for item in queryset]

    # Create a scatter plot for Form 2
    fig = go.Figure(data=go.Scatter(x=start_years, y=intensities, mode='markers'))
    fig.update_layout(title='Intensity vs. Start Year ')

    # Convert the chart to HTML for Form 2
    chart_html = opy.plot(fig, auto_open=False, output_type='div')

    return chart_html


def component_Year(request):
    # Get the list of unique values for End Year, Intensity, and Start Year
    end_years1 = InternData.objects.values_list('end_year', flat=True).distinct()
    intensities1 = InternData.objects.values_list('intensity', flat=True).distinct()
    start_years1 = InternData.objects.values_list('start_year', flat=True).distinct()

    # Check which form was submitted
    if 'filter-end-year' in request.GET or 'filter-intensity' in request.GET:
        chart_html = filter_form1(request)
    elif 'filter-start-year2' in request.GET or 'filter-intensity2' in request.GET:
        chart_html = filter_form2(request)
    else:
        chart_html = None  # No form submitted, set chart_html to None

    context = {
        'end_years': end_years1,
        'intensities': intensities1,
        'start_years': start_years1,
        'chart_html': chart_html,
    }

    return render(request, 'component_Year.html', context)



def component_Intensity(request):
   

    # Fetch the data you want to display in the chart
    data = list(InternData.objects.values('start_year', 'sector','intensity'))
 
    
    data1 = InternData.objects.all().order_by('end_year')
    
    # Extract the 'start_year' and 'intensity' values from the data
    end_years = [entry.end_year for entry in data1]
    intensities = [entry.intensity for entry in data1]

    # Create the line chart
    plt.figure(figsize=(10, 6))
    plt.plot(end_years, intensities, marker='o')
    plt.xlabel('end Year')
    plt.ylabel('Intensity')
    plt.title('Line Chart of Intensity Over Time')

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the chart as a base64 string for embedding in HTML
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    context = {
       
        'intensity_data_json': json.dumps(data),  # Convert data to JSON
      
        'chart_data': chart_data,
    }
    return render(request,'component_Intensity.html',context)

def component_Country(request):
    regions = InternData.objects.values_list('region', flat=True).distinct()
    countrys = InternData.objects.values_list('country', flat=True).distinct()
    topics = InternData.objects.values_list('topic', flat=True).distinct()
    sectors = InternData.objects.values_list('sector', flat=True).distinct()

# Filter out empty or invalid entries from the list
   
    selected_region = request.GET.get('filter-Region')
    selected_country = request.GET.get('filter-Country')
 
    selected_topic = request.GET.get('filter-topic')
    selected_sector = request.GET.get('filter-sector')

    queryset = InternData.objects.all()
    if selected_region:
        queryset = queryset.filter(region=selected_region)

    if selected_country:
        queryset = queryset.filter(country=selected_country)


    if selected_topic:
        queryset = queryset.filter(topic=selected_topic)

    if selected_sector:
        queryset = queryset.filter(sector=selected_sector)

    data = pd.DataFrame(list(queryset.values()))
    if 'topic' in data.columns:
    # Create a new column that concatenates topic and country information
        data['hover_info'] = data['topic'] + ' in ' + data['country']
    else:
        data['hover_info'] = 'none topic'
    # Create a choropleth map using Plotly Express with custom hover information
    if 'country' in data.columns:
        fig = px.choropleth(data_frame=data,
                        locations='country',  # Country data
                        locationmode='country names',
                        color='sector',  # Color by sector
                        hover_name='hover_info',  # Custom hover information
                        title='Sector Distribution by Country')
        chart_html = fig.to_html()
    else:
    # Handle the case where 'country' column is missing
        chart_html = 'no data' 

    context = {
        'regions': regions,
        'countrys': countrys,
        'topics': topics,
        'sectors':sectors,
        'chart_html': chart_html
    }


    return render(request,'component_Country.html',context)



def component_Region(request):
    total_entries_count = InternData.objects.count()

    # Fetch the data you want to display in the chart
    region_data = InternData.objects.values('region').annotate(data_count=models.Count('id'))

    # Prepare the data for the pie chart
    labels = [entry['region'] for entry in region_data]
    data_counts = [entry['data_count'] for entry in region_data]
    
    
    # Encode the chart as a base64 string for embedding in HTML
   
    context = {
        'total_entries_count': total_entries_count,
      
        'labels': labels,
        'data_counts': data_counts,
      
    }
    return render(request,'component_Region.html',context)

def component_City(request):
    return render(request,'component_City.html')
