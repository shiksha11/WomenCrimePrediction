
from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    return render(request,"home.html")

def temphome(request):
    return render(request,"tmp_home.html")

def fin(request):
    input_lat = float(request.GET['latitude'])
    input_long = float(request.GET['longitude'])

    ouput = compare(input_lat, input_long)
    return render(request,"final.html")

def predict(request):
    return render(request,"predict.html")

def aboutpage(request):
    return render(request, "about.html")

def visualizedata(request):
    return render(request, "visualization.html")

import sys

#---------------COMPARE FILES ---------------------


def compare(input_lat, input_long):
    
    import pandas as pd
    import math
    import pickle
    import numpy as np
    
    # Read Criminal & Districts Files
    criminalData_path = r'/Users/shiksharawat/Desktop/hack/womencrime/data/CriminalRecords.csv'
    df_criminal = pd.read_csv(criminalData_path)
    
    districtsData_path = r'/Users/shiksharawat/Desktop/hack/womencrime/data/DistrictsData.csv'
    df_district = pd.read_csv(districtsData_path)
    
    # Data Pre-Processing
    df_district['Name'] = df_district['Name'].str.lower()
    df_district.loc[df_district['Name'] == 'khandwa (east nimar)', 'Name']  = 'khandwa'
    df_district.loc[df_district['Name'] == 'khargone (west nimar)', 'Name'] = 'khargone'
    df_criminal['District'] = df_criminal['District'].str.lower()
    
    merged_df = pd.merge(left=df_district, right=df_criminal, left_on='Name', right_on='District', how='right')
    merged_df.dropna(inplace=True)
    
    # Merging with Coordinates
    coordinates_path = r'/Users/shiksharawat/Desktop/hack/womencrime/data/MPCoordinates.csv'
    df_coordinates = pd.read_csv(coordinates_path)
    df_coordinates['State'] = df_coordinates['State'].str.lower()
    merged_df = pd.merge(left=merged_df, right=df_coordinates, left_on='Name', right_on='State', how='left')
    
    merged_df.drop(columns=['State_x', 'District_x', 'Subdistt', 'Town/Village', 'Ward', 'EB', 'Level', 'TRU', 'District_y', 'Category', 'State_y'],inplace=True)
    
    classes = ['Rape', 'Kidnap', 'Sexual Harassment', 'Others']
    for c in classes:
        merged_df[c] = 0
        
    merged_df.loc[merged_df['Acts'].str.contains("376", case=False), 'Rape'] = 1
    merged_df.loc[merged_df['Acts'].str.contains("360", case=False), 'Kidnap'] = 1
    merged_df.loc[merged_df['Acts'].str.contains("366", case=False), 'Kidnap'] = 1
    merged_df.loc[merged_df['Acts'].str.contains("359", case=False), 'Kidnap'] = 1
    
    merged_df.loc[merged_df['Acts'].str.contains("354", case=False), 'Sexual Harassment'] = 1
    
    merged_df.loc[(merged_df['Rape'] == 0) & (merged_df['Kidnap'] == 0) 
                  & (merged_df['Sexual Harassment'] == 0), 'Others'] = 1
    
    merged_df.drop(columns=['Name','Acts','Index','No_of_Accused'],inplace=True)
    
    #-----------------Unique State Files -------------------------
    
    classes = ['Rape', 'Kidnap', 'Sexual Harassment', 'Others']
    y = merged_df[classes]
    x = merged_df.drop(columns=classes)
    
    x = x.drop_duplicates()
    x = x.drop(columns=['Unnamed: 3','Unnamed: 4'])
    min_dist = float('inf')
    print(x.head(5))
    
    if input_lat < 21 or input_lat > 26 or input_long < 74 and input_long > 82:
        return 'Not in Range'
    
    for index,row in x.iterrows():
        
        lat  = row['Latitude']
        long = row['Longitude']
        
        dist = math.sqrt((lat - input_lat)**2 + (long - input_long)**2)
        
        if dist < min_dist:
          min_dist = dist
          result = row.copy()
          result['Latitude'] = input_lat
          result['Longitude'] = input_long


    test_input = result.values.reshape(1,-1)
    print(test_input.shape)
    normalized_result=(test_input-test_input.min())/(test_input.max()-test_input.min())
    normalized_result = np.asarray(normalized_result).astype(np.float32)

    #normalized_result = normalized_result.reshape(1,-1)
    
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(normalized_result)
    return result