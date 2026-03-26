
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from learnin.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login as auth_login,logout as logout_nik
from learnin.models import Categories,Course,Level,Video,UserCourse ,Payment
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required






def BASE(request):
    return render(request,'base.html')

def home(request):
    category = Categories.objects.all().order_by('id')[0:6]
    course = Course.objects.filter(status = 'PUBLISH').order_by('id')

    context = {
        'category':category,
        'course':course
    }
    return render(request,'main/home.html',context)
def single_course(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context = {
         'category':category,
         'level':level,
         'course':course,
        'FreeCourse_count':FreeCourse_count,
        'PaidCourse_count':PaidCourse_count,
    }

    return render(request,'main/single_course.html',context)


def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price=request.GET.getlist('price[]')

    if price ==['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price ==['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['priceAll']:
        course = Course.objects.all()

    elif category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')

    else:
        course = Course.objects.all().order_by('-id')
    context = {
        'course': course,

    }

    t = render_to_string('ajax/course.html', context)
    return JsonResponse({'data': t})



def contact_us(request):
    category = Categories.get_all_category(Categories)
    context={
        'category':category,
    }
    return render(request,'main/contact_us.html',context)

def about_us(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request,'main/about_us.html',context)


def login(request):

    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request,'main/login.html',context)

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # check email
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email are Already Exists !')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username are Already exists !')
            return redirect('register')

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'main/register.html')

def do_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next')   # ✅ next parameter pakdo

        user = EmailBackEnd.authenticate(request,
                                         username=email,
                                         password=password)
        if user is not None:
            auth_login(request, user)
            # ✅ agar next_url mila to wahi redirect karo
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password Are Invalid !')
            return redirect('login')



def singin(request):

    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request, 'main/singin.html',context)

def logout(request):
    logout_nik (request)
    messages.success(request, 'You are logged out!')
    return redirect('home')

def Profile(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request, 'registration/profile.html',context)


def profile_update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email


        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile Are Successfully Updated. ')
        return redirect('profile')

def Search_Course(request):
    query = request.GET['query']
    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(title__icontains = query)
    context={
        'category': category,
        'course':course,
    }
    return render(request,'search/search.html',context)


def COURSE_DETAILS(request,slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))




    course = Course.objects.filter(slug=slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    context = {
        'category': category,
        'course':course,
        'time_duration':time_duration,


    }

    return render(request,'course/course_details.html',context)


def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request,'error/404.html',context)
@login_required
def checkout(request, slug):   # <-- नाम बदल दिया
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')
    order = None

    # Free course enrollment
    if course.price == 0:
        UserCourse.objects.create(
            user=request.user,
            course=course,
        )
        messages.success(request, 'Course Successfully Enrolled.')
        return redirect('my_course')

    # Paid course checkout
    elif action == 'create_payment':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')

            amount = (course.price * 100)
            currency = "INR"
            notes = {
                "name": f'{first_name} {last_name}',
                "email": email,
            }

            receipt = f"SKola-{int(time())}"
            order = client.order.create({
                'receipt': receipt,
                'notes': notes,
                'amount': amount,
                'currency': currency,
            })

            Payment.objects.create(
                course=course,
                user=request.user,
                order_id=order.get('id')
            )

    context = {
        'course': course,
        'order': order,
    }
    return render(request, 'checkout/checkout.html', context)



@login_required
def MY_COURSE(request):
    course = UserCourse.objects.filter(user=request.user)
    context = {
        'course': course,
    }
    return render(request, 'course/mycourse.html', context)



@csrf_exempt
@login_required
def VERIFY_PAYMENT(request):
    if request.method == "POST":
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercourse = UserCourse.objects.create(
                user=payment.user,
                course=payment.course,
            )
            payment.user_course = usercourse
            payment.save()

            context = {
                'data': data,
                'payment': payment,
            }
            return render(request, 'verify_payment/success.html', context)
        except:
            return render(request, 'verify_payment/fail.html')