from django.shortcuts import render
from .models import Service, Product, Career
from django.core.mail import send_mail 

# Create your views here.
def home(request):

    ser1 = Service()
    ser1.img = 'gear.svg'
    ser1.desc = "END to END IT and Engineering Services"

    ser2 = Service()
    ser2.img = 'person-bounding-box.svg'
    ser2.desc = "Complete Support to Existing Business Processes"

    ser3 = Service()
    ser3.img = 'hand-thumbs-up.svg'
    ser3.desc = "Trustworthy Business Consultation"

    ser4 = Service()
    ser4.img = 'ui-checks-grid.svg'
    ser4.desc = "Expert Engineering Consultation"

    servs = [ser1, ser2, ser3, ser4]

    prods = Product.objects.all()

    return render(request, "home/home.html", {'servs' : servs, 'prods' : prods})

def careers(request):

    # car1 = Careers()
    # car1.img = 'career-1.jpg'
    # car1.head = 'Software Development Engineers'
    # car1.desc = 'We are always on a lookout for Software Development Engineers who want to think out of the box and who want to work in critical embedded domains. Just send us your interest and your latest resume and we will get back to you'

    # car2 = Careers()
    # car2.img = 'career-2.jpg'
    # car2.head = 'Software Test Engineers'
    # car2.desc = 'We are always on a lookout for Software Test Engineers who strive hard to break the system in any logical way possible by staying within the requirement limits. Just send us your interest and your latest resume and we will get back to you.'

    # car3 = Careers()
    # car3.img = 'career-3.jpg'
    # car3.head = 'Technical Architects'
    # car3.desc = 'Do you feel you are intrigued by what we do ? Would you like to know more and would like to add value to our organization ? We will be delighted to discuss your candidature.&nbsp;Just send us your interest and your latest resume and we will get back to you.'

    # cars = [car1, car2, car3]

    cars = Career.objects.all()

    return render(request, "home/careers.html", { 'cars' : cars })

def contact(request):
    if request.method == 'POST':
        email = request.POST['from-email']
        name = request.POST['from-name']
        phone = request.POST['from-phone']
        msg = request.POST['from-message']
        data = {'name' : name, 'email': email, 'phone': phone, 'msg': msg}
        message = '''
        Name: {}

        From: {}

        Phone Number: {}

        Message: {}
        '''.format(data['name'], data['email'], data['phone'], data['msg'])
        send_mail(name, message, '', ['dummyhrms2022@gmail.com'])
        return render(request, "home/contact.html", {'name' : name})
    else:
        return render(request, "home/contact.html")

def industries(request):
    return render(request, "home/industries.html")

def technologies(request):
    return render(request, "home/technologies.html")

def services(request):
    return render(request, "home/services.html")

def aboutus(request):
    if request.method == 'POST':
        email = request.POST['from-email']
        name = request.POST['from-name']
        phone = request.POST['from-phone']
        msg = request.POST['from-message']
        data = {'name' : name, 'email': email, 'phone': phone, 'msg': msg}
        message = '''
        Name: {}

        From: {}

        Phone Number: {}

        Message: {}
        '''.format(data['name'], data['email'], data['phone'], data['msg'])
        send_mail(name, message, 'dummyhrms2022@gmail.com', ['jayanthkumar.singh@crestaerospace.com'])
        return render(request, "home/aboutus.html", {'name' : name})
    else:
        return render(request, "home/aboutus.html")

def sitemap(request):
    return render(request, "home/sitemap.html")