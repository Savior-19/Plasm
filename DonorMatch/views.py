from django.shortcuts import render

# Create your views here.


def HomePage(request) :
    return render(request, 'home.html')


#@login_required
def DonorSearch(request) :
    if request.method == 'GET' :
        return render(request, 'search.html', {'display_data':False})
    else :
        context = {'display_data':True}

        # Recieve data from form
        blood_abo = request.POST['abo']
        blood_rh = request.POST['rh']
        city = request.POST['city']
        district = request.POST['district']
        state = request.POST['state']

        # Perform api calls here

        return render(request, 'search.html', context)
