from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import APICalls

import requests
import threading
import string
import math
import time

# Create your views here.


def HomePage(request) :
    return render(request, 'home.html')


patient_data = []
patient_data_lock = threading.Lock()


def serial_task(hospitals, blood_requirement) :
    """ Performs the serial task of making the api calls and storing the information in an array. """
    global patient_data
    patient_data_thread_local = []
    for hospital in hospitals :
        url = hospital.api_url
        url = string.Template(url).substitute(**blood_requirement)
        response = requests.get(url).json()
        for i in range(len(response)) :
            current_data = response[i]
            current_data["hospital"] = "Plasm_Hospital 1"
            data_arr = [
                current_data["blood_abo_type"],
                current_data["blood_rh_type"],
                hospital.hospital_name,
                "Recovered",
                current_data["age_bracket"],
                current_data["gender"],
                current_data["nationality"],
                current_data["city"]
            ]
            patient_data_thread_local.append(data_arr)
    
    # Acquire the lock
    patient_data_lock.acquire()
    # Make the additions to the main list of patient data
    patient_data = patient_data + patient_data_thread_local
    # Release the lock
    patient_data_lock.release()


#@login_required
def DonorSearch(request) :
    if request.method == 'GET' :
        return render(request, 'search.html', {'display_data':False})
    else :
        global patient_data
        patient_data = []

        # Recieve data from the html-form
        blood_requirement = {
            'blood_abo' : request.POST['abo'],
            'blood_rh' : request.POST['rh'],
            'city' : " " if request.POST['city'] == "" else request.POST['city'],
            'district' : " " if request.POST['district'] == "" else request.POST['district'],
            'state' : " " if request.POST['district'] == "" else request.POST['district']
        }

        
        # Perform api calls here

        # Get the hospital details from the database
        hospital_details = APICalls.objects.all()
        num_threads = 2
        thread_job_pool = []
        # Start of the parallel execution
        parallel_execution_start = time.time()
        thread_max_num_jobs = math.ceil(len(hospital_details) / num_threads)
        for i in range(num_threads) :
            thread_job_pool.append(hospital_details[(i * thread_max_num_jobs) : min(((i+1) * thread_max_num_jobs), len(hospital_details))])
        print(thread_job_pool)

        # Sample URL Pattern
        #url = "http://127.0.0.1:8000/api/patient_details/abo=$blood_abo&rh=$blood_rh&city=$city&district=$district&state=$state"
        #url = "http://127.0.0.1:8000/api/patient_details/abo=" + blood_abo + "&rh=" + blood_rh + "&city=" + (" " if city == "" else city) + "&district=" + (" " if district == "" else district) + "&state=" + (" " if state == "" else state)
        

        # Threading setup
        execution_start_time = time.time()
        threads = []
        for i in range(num_threads-1) :
            # Execution of the serial task
            t = threading.Thread(target=serial_task, args=(thread_job_pool[i], blood_requirement))
            threads.append(t)
            t.start()
        # Execution of the serial task for the master thread
        serial_task(thread_job_pool[-1], blood_requirement)
        execution_end_time = time.time()
        for i in range(num_threads-1) :
            threads[i].join()
        parallel_execution_end = time.time()

        # Calculate the time taken
        #print("Time taken for the total parallel execution : ", (parallel_execution_end - parallel_execution_start))
        print("Time taken for the parallel execution alone : ", (execution_end_time - execution_start_time))
        print("Time taken for the setup process for the threads (the additional overhead due to threading) : ", (execution_start_time - parallel_execution_start))

        # """
        # In case we need to demonstrate the serial execution
        serial_execution_start = time.time()
        parform_task_serially(hospital_details, blood_requirement)
        serial_execution_end = time.time()

        print("TIme taken for Serial Execution : ", (serial_execution_end - serial_execution_start))
        # """


        # Return the values to the web page
        context = {'display_data':True, 'patient_data':patient_data, 'num_patients':len(patient_data)}
        return render(request, 'search.html', context)




def parform_task_serially(hospitals, blood_requirement) :
    """
        Performs the serial task of making the api calls and storing the information in an array.
        This is done in a serial manner without using threads.
    """
    patient_data = []
    for hospital in hospitals :
        url = hospital.api_url
        url = string.Template(url).substitute(**blood_requirement)
        response = requests.get(url).json()
        for i in range(len(response)) :
            current_data = response[i]
            current_data["hospital"] = "Plasm_Hospital 1"
            data_arr = [
                current_data["blood_abo_type"],
                current_data["blood_rh_type"],
                hospital.hospital_name,
                "Recovered",
                current_data["age_bracket"],
                current_data["gender"],
                current_data["nationality"],
                current_data["city"]
            ]
            patient_data.append(data_arr)
