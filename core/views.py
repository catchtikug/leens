from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SideEffectForm, DrugResistanceForm

# def home_view(request):
#     return render(request, 'core/home.html')


# def login_view(request):
#     form = LoginForm(request.POST or None)
#     if form.is_valid():
#         user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
#         if user:
#             login(request, user)
#             return redirect('dashboard')
#     return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    user = request.user
    logout(user)
    return redirect(request, 'login')


# from django.db.models import Count
# from .models import SideEffectReport

# 
# def dashboard_view(request):
#     # Side effect counts
#     effect_data = (SideEffectReport.objects
#                    .values('side_effects')
#                    .annotate(count=Count('side_effects'))
#                    .order_by('-count')[:5])

#     # Suspected drug counts
#     drug_data = (SideEffectReport.objects
#                  .values('suspected_drug')
#                  .annotate(count=Count('suspected_drug'))
#                  .order_by('-count')[:5])

#     return render(request, 'core/dashboard.html', {
#         'effect_data': effect_data,
#         'drug_data': drug_data,
#     })



# 
# def submit_side_effect(request):
#     form = SideEffectForm(request.POST or None)
#     if form.is_valid():
#         report = form.save(commit=False)
#         report.user = request.user
#         report.save()
#         return redirect('dashboard')
#     return render(request, 'core/side_effect.html', {'form': form})


# 
# def submit_drug_resistance(request):
#     form = DrugResistanceForm(request.POST or None)
#     if form.is_valid():
#         report = form.save(commit=False)
#         report.user = request.user
#         report.save()
#         return redirect('dashboard')
#     return render(request, 'core/drug_resistance.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import LoginForm, SideEffectForm, DrugResistanceForm
from .models import SideEffectReport, DrugResistanceReport, Drug, Disease, Facility,  User

def home_view(request):
    """Render the home page with statistics and featured content"""
    # Get some statistics for the home page
    side_effect_count = SideEffectReport.objects.count()
    resistance_count = DrugResistanceReport.objects.count()
    facility_count = Facility.objects.count()
    
    # Get recent reports for display
    recent_side_effects = SideEffectReport.objects.select_related('user').order_by('-created_at')[:3]
    recent_resistance = DrugResistanceReport.objects.select_related('user').order_by('-created_at')[:3]
    
    context = {
        'side_effect_count': side_effect_count,
        'resistance_count': resistance_count,
        'facility_count': facility_count,
        'recent_side_effects': recent_side_effects,
        'recent_resistance': recent_resistance,
    }
    return render(request, 'core/home.html', context)

def login_view(request):
        
    form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form})


def dashboard_view(request):
    """Admin dashboard with statistics and quick actions"""
    # Side effect statistics
    effect_data = (SideEffectReport.objects
                 .values('side_effects')
                 .annotate(count=Count('side_effects'))
                 .order_by('-count')[:5])
    
    # Suspected drug statistics
    drug_data = (SideEffectReport.objects
               .values('suspected_drug')
               .annotate(count=Count('suspected_drug'))
               .order_by('-count')[:5])
    
    # Resistance statistics
    resistance_data = (DrugResistanceReport.objects
                      .values('same_disease')
                      .annotate(count=Count('same_disease'))
                      .order_by('-count')[:3])
    
    # Recent activity
    recent_side_effects = SideEffectReport.objects.order_by('-created_at')[:5]
    recent_resistance = DrugResistanceReport.objects.order_by('-created_at')[:5]
    
    # User-specific data if needed
    user = User.objects.first()
    user_reports = {
        'side_effects': SideEffectReport.objects.filter(user=user).count(),
        'resistance': DrugResistanceReport.objects.filter(user=user).count(),
    }
    
    context = {
        'effect_data': effect_data,
        'drug_data': drug_data,
        'resistance_data': resistance_data,
        'recent_side_effects': recent_side_effects,
        'recent_resistance': recent_resistance,
        'user_reports': user_reports,
        'drugs': Drug.objects.all()[:10],  # For dropdowns or autocomplete
        'diseases': Disease.objects.all()[:10],
    }
    return render(request, 'core/dashboard.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SideEffectForm
from .models import Drug

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    return render(request, 'core/contact.html')

def submit_side_effect(request):
    if request.method == 'POST':
        form = SideEffectForm(request.POST)
        if form.is_valid():
            try:
                # Save the form with user information
                report = form.save(commit=False)
                report.user = request.user
                report.save()
                
                # Add success message
                messages.success(
                    request,
                    f"Successfully reported side effects for {report.suspected_drug}. "
                    "Thank you for contributing to medication safety!"
                )
                return redirect('dashboard')
                
            except Exception as e:
                # Handle any database errors
                messages.error(
                    request,
                    "An error occurred while saving your report. Please try again."
                )
                # Log the error for debugging
                print(f"Error saving side effect report: {str(e)}")
    else:
        form = SideEffectForm()
    
    # Get drug suggestions for autocomplete
    drug_suggestions = Drug.objects.values_list('name', flat=True)[:10]  # Limit to 10
    
    context = {
        'form': form,
        'drug_suggestions': list(drug_suggestions),
    }
    return render(request, 'core/side_effect.html', context)


def submit_drug_resistance(request):
    """Handle drug resistance report submission"""
    if request.method == 'POST':
        form = DrugResistanceForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, "Drug resistance report submitted successfully!")
            return redirect('dashboard')
    else:
        form = DrugResistanceForm()
    
    # Add diseases list for autocomplete suggestions
    diseases = Disease.objects.values_list('name', flat=True)
    drugs = Drug.objects.values_list('name', flat=True)
    
    context = {
        'form': form,
        'diseases': list(diseases),
        'drugs': list(drugs),
    }
    return render(request, 'core/drug_resistance.html', context)