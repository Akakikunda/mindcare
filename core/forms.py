from django import forms
from .models import CustomUser
from .models import Appointment
from .models import Assessment
from .models import Message
from django.contrib.auth import get_user_model
from .models import Appointment, CustomUser





class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['therapist', 'date', 'time', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['therapist'].queryset = CustomUser.objects.filter(role='therapist')
        
      

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['category', 'score']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']


class AssessmentForm(forms.Form):
    QUESTION_CHOICES = [
        (1, 'Strongly Disagree'),
        (2, 'Disagree'),
        (3, 'Neutral'),
        (4, 'Agree'),
        (5, 'Strongly Agree'),
    ]

    category = forms.ChoiceField(choices=[('anxiety', 'Anxiety')], widget=forms.HiddenInput())

    q1 = forms.ChoiceField(label="I often feel nervous", choices=QUESTION_CHOICES, widget=forms.RadioSelect)
    q2 = forms.ChoiceField(label="I struggle to relax", choices=QUESTION_CHOICES, widget=forms.RadioSelect)
    q3 = forms.ChoiceField(label="I have trouble sleeping", choices=QUESTION_CHOICES, widget=forms.RadioSelect)
    q4 = forms.ChoiceField(label="I feel overwhelmed", choices=QUESTION_CHOICES, widget=forms.RadioSelect)



CustomUser = get_user_model()

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'specialty', 'location', 'bio']



class IndividualAssessmentForm(forms.Form):
    stress_level = forms.ChoiceField(
        label="How often do you feel stressed?",
        choices=[('1', 'Rarely'), ('2', 'Sometimes'), ('3', 'Often'), ('4', 'Always')],
        widget=forms.RadioSelect
    )

    sleep_quality = forms.ChoiceField(
        label="How would you rate your sleep quality?",
        choices=[('1', 'Very good'), ('2', 'Good'), ('3', 'Poor'), ('4', 'Very poor')],
        widget=forms.RadioSelect
    )

    focus_level = forms.ChoiceField(
        label="How well can you focus on tasks?",
        choices=[('1', 'Very well'), ('2', 'Okay'), ('3', 'Not well'), ('4', 'Not at all')],
        widget=forms.RadioSelect
    )

    mood = forms.ChoiceField(
        label="How often do you feel low or sad?",
        choices=[('1', 'Rarely'), ('2', 'Sometimes'), ('3', 'Often'), ('4', 'Always')],
        widget=forms.RadioSelect
    )
    

class FamilyAssessmentForm(forms.Form):
    stress_level = forms.ChoiceField(
        label="How often do you feel stressed?",
        choices=[('1', 'Rarely'), ('2', 'Sometimes'), ('3', 'Often'), ('4', 'Always')],
        widget=forms.RadioSelect
    )

    sleep_quality = forms.ChoiceField(
        label="How would you rate your sleep quality?",
        choices=[('1', 'Very good'), ('2', 'Good'), ('3', 'Poor'), ('4', 'Very poor')],
        widget=forms.RadioSelect
    )

    focus_level = forms.ChoiceField(
        label="How well can you focus on tasks?",
        choices=[('1', 'Very well'), ('2', 'Okay'), ('3', 'Not well'), ('4', 'Not at all')],
        widget=forms.RadioSelect
    )

    mood = forms.ChoiceField(
        label="How often do you feel low or sad?",
        choices=[('1', 'Rarely'), ('2', 'Sometimes'), ('3', 'Often'), ('4', 'Always')],
        widget=forms.RadioSelect
    )


class CoupleAssessmentForm(forms.Form):
    stress_level = forms.ChoiceField(
        label="How often do you feel stressed?",
        choices=[('1', 'Rarely'), ('2', 'Sometimes'), ('3', 'Often'), ('4', 'Always')],
        widget=forms.RadioSelect
    )

    sleep_quality = forms.ChoiceField(
        label="How would you rate your sleep quality?",
        choices=[('1', 'Very good'), ('2', 'Good'), ('3', 'Poor'), ('4', 'Very poor')],
        widget=forms.RadioSelect
    )

    focus_level = forms.ChoiceField(
        label="How well can you focus on tasks?",
        choices=[('1', 'Very well'), ('2', 'Okay'), ('3', 'Not well'), ('4', 'Not at all')],
        widget=forms.RadioSelect
    )

    mood = forms.ChoiceField(
        label="How often do you feel low or sad?",
        choices=[('1', 'Rarely'), ('2', 'Sometimes'), ('3', 'Often'), ('4', 'Always')],
        widget=forms.RadioSelect
    )


class TeenAssessmentForm(forms.Form):
    stress_level = forms.ChoiceField(
        label="How often do you feel stressed?",
        choices=[('1', 'Rarely'), ('2', 'Sometimes'), ('3', 'Often'), ('4', 'Always')],
        widget=forms.RadioSelect
    )

    sleep_quality = forms.ChoiceField(
        label="How would you rate your sleep quality?",
        choices=[('1', 'Very good'), ('2', 'Good'), ('3', 'Poor'), ('4', 'Very poor')],
        widget=forms.RadioSelect
    )

    focus_level = forms.ChoiceField(
        label="How well can you focus on tasks?",
        choices=[('1', 'Very well'), ('2', 'Okay'), ('3', 'Not well'), ('4', 'Not at all')],
        widget=forms.RadioSelect
    )

    mood = forms.ChoiceField(
        label="How often do you feel low or sad?",
        choices=[('1', 'Rarely'), ('2', 'Sometimes'), ('3', 'Often'), ('4', 'Always')],
        widget=forms.RadioSelect
    )






        
