from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import requests

# Create your views here.


def HomePage(request) :
    return render(request, 'home.html')


#@login_required
def DonorSearch(request) :
    if request.method == 'GET' :
        return render(request, 'search.html', {'display_data':False})
    else :
        # Recieve data from the form
        blood_abo = request.POST['abo']
        blood_rh = request.POST['rh']
        city = request.POST['city']
        district = request.POST['district']
        state = request.POST['state']

        # Perform api calls here
        url = "http://127.0.0.1:8000/api/patient_details/abo=" + blood_abo + "&rh=" + blood_rh + "&city=" + (" " if city == "" else city) + "&district=" + (" " if district == "" else district) + "&state=" + (" " if state == "" else state)
        response = requests.get(url).json()
        patient_objects = []
        for i in range(len(response)) :
            current_data = response[i]
            current_data["hospital"] = "Plasm_Hospital 1"
            data_arr = [
                current_data["blood_abo_type"],
                current_data["blood_rh_type"],
                "Plasm_Hospital 1",
                "Recovered",
                current_data["age_bracket"],
                current_data["gender"],
                current_data["nationality"],
                current_data["city"]
            ]
            patient_objects.append(data_arr)


        # Return the values to the web page

        context = {'display_data':True, 'patient_data':patient_objects, 'num_patients':len(patient_objects)}
        return render(request, 'search.html', context)
