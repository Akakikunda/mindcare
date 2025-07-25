from django.shortcuts import render, redirect
from .models import Resource
from django.contrib.auth import login
from .forms import RegisterForm
from .forms import AppointmentForm
from .models import Appointment
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from .forms import ProfileForm
from .models import Assessment
from .forms import AssessmentForm
from .forms import MessageForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Appointment, Message, Resource
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .forms import CustomUserChangeForm
from .models import CustomUser  # if CustomUser is your therapist model
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .forms import IndividualAssessmentForm
from .forms import FamilyAssessmentForm
from .forms import TeenAssessmentForm
from .forms import CoupleAssessmentForm
from django.http import HttpResponse
from .models import Appointment
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Appointment, Assessment, Resource, CustomUser
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .models import Appointment, Assessment, Resource, CustomUser
from .forms import ResourceForm  # Make sure you have this form
from .models import Resource
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import Appointment
from .models import Appointment, Resource  # Update if your model names differ
from django.contrib.auth.decorators import login_required
from .models import Assessment  # Make sure Assessment model exists
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm






@login_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')


@login_required
def notifications_view(request):
    return render(request, 'core/notifications.html')

@login_required
def profile_view(request):
    return render(request, 'core/profile.html')

def logout_view(request):
    django_logout(request)
    return redirect('login')  # or use your landing page


#def custom_login(request):
    #if request.method == 'POST':
        #user = authenticate(
            #request,
           # username=request.POST['username'],
         #   password=request.POST['password']
        #)
     #   if user is not None:
     #       login(request, user)
    #        return redirect('home')  # or 'dashboard'
   # return render(request, 'login.html')


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ✅ Redirect based on role
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.role == 'therapist':
                return redirect('therapist_dashboard')
            elif user.role == 'client':
                return redirect('dashboard')  # or 'client_dashboard'
            else:
                return redirect('home')  # fallback
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})




def landing_page(request):
    return render(request, 'core/landing.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})



def projects_view(request):
    return render(request, 'core/projects.html')




def resources_view(request):
    resources = Resource.objects.all()
    return render(request, 'core/resources.html', {'resources': resources})



def assessments_view(request):
    assessments = Assessment.objects.all()
    return render(request, 'core/assessments.html', {'assessments': assessments})





@login_required
def home_view(request):
    appointments = Appointment.objects.filter(client=request.user)
    resources = Resource.objects.all()[:3]  # Just show latest 3
    projects = Project.objects.all()[:3]
    
    return render(request, 'core/home.html', {
        'appointments': appointments,
        'resources': resources,
        'projects': projects,
    })



def home_view(request):
    projects = Project.objects.all()
    resources = Resource.objects.all()
    appointments = Appointment.objects.filter(user=request.user) if request.user.is_authenticated else []

    context = {
        'projects': projects,
        'resources': resources,
        'appointments': appointments,
    }
    return render(request, 'core/home.html', context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'core/profile.html', {'form': form})


def home_view(request):
    return render(request, 'core/home.html')


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    return render(request, 'core/book_appointment.html', {'form': form})

def appointment_success(request):
    return render(request, 'core/appointment_success.html')



@login_required
def take_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.user = request.user
            assessment.save()
            return redirect('my_assessments')
    else:
        form = AssessmentForm()
    return render(request, 'core/take_assessment.html', {'form': form})

@login_required
def my_assessments(request):
    assessments = Assessment.objects.filter(user=request.user)
    return render(request, 'core/my_assessments.html', {'assessments': assessments})


def view_resources(request):
    resources = Resource.objects.all().order_by('-created_at')
    return render(request, 'core/resources.html', {'resources': resources})

def therapist_directory(request):
    therapists = CustomUser.objects.filter(role='therapist')
    query = request.GET.get('q')
    if query:
        therapists = therapists.filter(
            Q(username__icontains=query) |
            Q(specialty__icontains=query) |
            Q(location__icontains=query)
        )
    return render(request, 'core/therapist_directory.html', {'therapists': therapists})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'core/send_message.html', {'form': form})

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'core/inbox.html', {'messages': messages})

def crisis_support(request):
    return render(request, 'core/crisis.html')



@login_required
def take_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            score = (
                int(form.cleaned_data['q1']) +
                int(form.cleaned_data['q2']) +
                int(form.cleaned_data['q3']) +
                int(form.cleaned_data['q4'])
            )
            assessment = Assessment.objects.create(
                user=request.user,
                category=form.cleaned_data['category'],
                score=score
            )
            return redirect('my_assessments')
    else:
        form = AssessmentForm(initial={'category': 'anxiety'})
    return render(request, 'core/take_assessment.html', {'form': form})

def view_resources(request):
    resources = Resource.objects.all()
    return render(request, 'core/resources.html', {'resources': resources})




User = get_user_model()

@staff_member_required
def admin_dashboard(request):
    users = CustomUser.objects.all()
    appointments = Appointment.objects.all()
    assessments = Assessment.objects.all()
    resources = Resource.objects.all()
    
    total_users = users.count()
    total_appointments = appointments.count()
    pending_appointments = appointments.filter(status='pending').count()
    total_assessments = assessments.count()
    recent_resources = resources.order_by('-created_at')[:5]

    context = {
        'users': users,
        'appointments': appointments,
        'assessments': assessments,
        'resources': resources,
        'total_users': total_users,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'total_assessments': total_assessments,
        'recent_resources': recent_resources,
    }

    return render(request, 'core/admin_dashboard.html', context)



def book_appointment(request):
    # after saving appointment:
    send_mail(
        'Appointment Confirmation',
        f'Dear {request.user.username}, your appointment has been booked.',
        'admin@mindcare.com',
        [request.user.email],
        fail_silently=True,
    )

@login_required
def therapist_dashboard(request):
    appointments = Appointment.objects.filter(therapist=request.user)
    messages = Message.objects.filter(receiver=request.user)
    resources = Resource.objects.filter(uploaded_by=request.user)
    
    return render(request, 'core/therapist_dashboard.html', {
        'appointments': appointments,
        'messages': messages,
        'resources': resources
    })
    

@login_required
def patient_profile(request):
    if request.user.role != 'patient':
        return redirect('home')  # Prevent access if not a patient

    return render(request, 'core/patient_profile.html', {'user': request.user})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('patient_profile' if request.user.role == 'patient' else 'therapist_dashboard')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})



@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'core/profile.html', {'form': form})


@login_required
def patient_profile_view(request):
    if request.user.role != 'client':
        return redirect('home')
    return render(request, 'core/patient_profile.html', {'user': request.user})


@staff_member_required
def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'core/manage_users.html', {'users': users})



User = get_user_model()

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:  # Prevent deleting self
        user.delete()
        messages.success(request, "User deleted successfully.")
    else:
        messages.warning(request, "You cannot delete your own admin account.")
    return redirect('manage_users')




def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on role
            if user.is_superuser:
                return redirect('/admin/')
            elif user.role == 'therapist':
                return redirect('therapist_dashboard')
            elif user.role == 'client':
                return redirect('patient_profile')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



def view_resources(request):
    resources = Resource.objects.all().order_by('-created_at')
    return render(request, 'core/resources.html', {'resources': resources})



def home_view(request):
    therapists = CustomUser.objects.filter(role='therapist')
    return render(request, 'core/home.html', {'therapists': therapists})



def therapist_profile_view(request, therapist_id):
    therapist = get_object_or_404(CustomUser, id=therapist_id, role='therapist')
    return render(request, 'core/therapist_profile.html', {'therapist': therapist})




@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, "Appointment booked successfully. Awaiting approval.")
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'core/book_appointment.html', {'form': form})



def individual_assessment(request):
    if request.method == 'POST':
        form = IndividualAssessmentForm(request.POST)
        if form.is_valid():
            total_score = sum(int(value) for value in form.cleaned_data.values())

            if total_score <= 6:
                result = "You're doing great, keep it up!"
            elif total_score <= 10:
                result = "You're doing okay, but check in with yourself."
            else:
                result = "You may benefit from speaking to a therapist."

            return render(request, 'core/assessments/individual_result.html', {
                'score': total_score,
                'result': result,
            })
    else:
        form = IndividualAssessmentForm()

    return render(request, 'core/assessments/individual.html', {'form': form})



def couple_assessment(request):
    if request.method == 'POST':
        form = CoupleAssessmentForm(request.POST)
        if form.is_valid():
            total_score = sum(int(value) for value in form.cleaned_data.values())

            if total_score <= 6:
                result = "You're doing great, keep it up!"
            elif total_score <= 10:
                result = "You're doing okay, but check in with yourself."
            else:
                result = "You may benefit from speaking to a therapist."

            return render(request, 'core/assessments/couple_result.html', {
                'score': total_score,
                'result': result,
            })
    else:
        form = CoupleAssessmentForm()

    return render(request, 'core/assessments/couple.html', {'form': form})



def family_assessment(request):
    if request.method == 'POST':
        form = FamilyAssessmentForm(request.POST)
        if form.is_valid():
            total_score = sum(int(value) for value in form.cleaned_data.values())

            if total_score <= 6:
                result = "You're doing great, keep it up!"
            elif total_score <= 10:
                result = "You're doing okay, but check in with yourself."
            else:
                result = "You may benefit from speaking to a therapist."

            return render(request, 'core/assessments/family_result.html', {
                'score': total_score,
                'result': result,
            })
    else:
        form = FamilyAssessmentForm()

    return render(request, 'core/assessments/family.html', {'form': form})


def teen_assessment(request):
    if request.method == 'POST':
        form = TeenAssessmentForm(request.POST)
        if form.is_valid():
            total_score = sum(int(value) for value in form.cleaned_data.values())

            if total_score <= 6:
                result = "You're doing great, keep it up!"
            elif total_score <= 10:
                result = "You're doing okay, but check in with yourself."
            else:
                result = "You may benefit from speaking to a therapist."

            return render(request, 'core/assessments/teen_result.html', {
                'score': total_score,
                'result': result,
            })
    else:
        form = TeenAssessmentForm()

    return render(request, 'core/assessments/teen.html', {'form': form})


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, "Appointment booked successfully. Awaiting approval.")
            return redirect('dashboard')  # or wherever your dashboard is
    else:
        form = AppointmentForm()
    return render(request, 'core/book_appointment.html', {'form': form})



@login_required
def therapist_dashboard(request):
    appointments = Appointment.objects.filter(therapist=request.user)
    return render(request, 'core/therapist_dashboard.html', {'appointments': appointments})

@login_required
def update_appointment_status(request, appointment_id, status):
    appointment = Appointment.objects.get(id=appointment_id)
    if appointment.therapist != request.user:
        return HttpResponseForbidden()
    appointment.status = status
    appointment.save()
    messages.success(request, f"Appointment marked as {status}.")
    return redirect('therapist_dashboard')



@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(client=request.user).order_by('-date')
    return render(request, 'core/client_dashboard.html', {'appointments': appointments})


def assessment_view(request):
    return render(request, 'core/assessment.html')


@login_required
def redirect_user_by_role(request):
    user = request.user

    if user.is_superuser:
        return redirect('admin_dashboard')  # You must have this URL name defined

    elif user.role == 'therapist':
        return redirect('therapist_dashboard')  # Must match your URL name

    elif user.role == 'client':
        return redirect('client_dashboard')  # Or use 'home' or a general page

    else:
        return redirect('home')  # Fallback just in case
    
    
#@login_required
#def role_redirect_view(request):
    #user = request.user
   # if user.is_superuser:
     #   return redirect('admin_dashboard')
    #elif user.role == 'therapist':
    #    return redirect('therapist_dashboard')
   # elif user.role == 'client':
  #      return redirect('home')  # or wherever your client lands
 #   else:
#       return redirect('home')
    
    from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def role_redirect_view(request):
    user = request.user

    # ✅ Check for superuser/admin
    if user.is_superuser:
        return redirect('admin_dashboard')

    # ✅ Check for therapist
    elif hasattr(user, 'role') and user.role == 'therapist':
        return redirect('therapist_dashboard')

    # ✅ Check for client
    elif hasattr(user, 'role') and user.role == 'client':
        return redirect('dashboard')  # or 'client_dashboard'

    # 🔁 Default fallback
    return redirect('home')



@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('admin_dashboard')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'core/edit_user.html', {'form': form, 'user': user})



@staff_member_required
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource uploaded successfully.")
            return redirect('admin_dashboard')
    else:
        form = ResourceForm()
    return render(request, 'core/upload_resource.html', {'form': form})




@user_passes_test(lambda u: u.is_superuser)
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ResourceForm()
    return render(request, 'core/upload_resource.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def edit_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'core/edit_resource.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    resource.delete()
    return redirect('admin_dashboard')




def appointments_view(request):
    appointments = Appointment.objects.all()
    return render(request, 'core/appointments.html', {'appointments': appointments})
