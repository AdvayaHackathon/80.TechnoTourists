#from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .models import Place
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import HiddenGem
from django.http import JsonResponse

def welcome(request):
    return render(request, 'heritage/welcome.html')

#def register_view(request):
    #if request.method == 'POST':
       # form = RegisterForm(request.POST)
        #if form.is_valid():
          #  form.save()
           # return redirect('login')
   # else:
        #form = RegisterForm()
   # return render(request, 'heritage/register.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto login user after registration
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')  # Make sure 'dashboard' URL is defined
    else:
        form = UserCreationForm()
    return render(request, 'heritage/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(request, username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'heritage/login.html')

def logout_view(request):
    logout(request)
    return redirect('welcome')

#def dashboard(request):
   # return render(request, 'heritage/dashboard.html')


@login_required
def dashboard(request):
    return render(request, 'heritage/dashboard.html')


def map_view(request):
    places = Place.objects.all()
    return render(request, 'heritage/map.html', {'places': places})

def etiquette_view(request):
    places = Place.objects.all()
    return render(request, 'heritage/etiquette.html', {'places': places})

def chatbot_view(request):
    response = "Hello! How can I assist you today?"  # Default response

    if request.method == 'POST':
        query = request.POST.get('query', '').lower()

        if "festival" in query or "event" in query:
            response = "🎉 You can check the Cultural Calendar page for upcoming festivals and events!"
        elif "respect" in query or "etiquette" in query:
            response = "🙏 Always respect local customs. Remove footwear at sacred places and dress modestly."
        elif "donate" in query or "support" in query:
            response = "💝 You can contribute to heritage preservation via the Donate page on our website."
        elif "hampi" in query:
            response = "🏛️ Hampi is a UNESCO World Heritage site known for its stunning ruins and ancient temples."
        elif "belur" in query:
            response = "⛩️ Belur is famous for the intricately carved Chennakesava Temple of the Hoysala dynasty."
        elif "badami" in query:
            response = "🪨 Badami is known for its rock-cut cave temples dating back to the 6th century."
        elif "heritage" in query or "culture" in query:
            response = "🌍 India has a rich cultural heritage! Explore our map and hidden gems itinerary to learn more."
        elif "food" in query or "cuisine" in query:
            response = "🍛 Don't miss local cuisines like Bisi Bele Bath in Karnataka or Dhokla in Gujarat!"
        elif "stay" in query or "accommodation" in query:
            response = "🏨 You can find stay options listed under each place’s description on the dashboard."
        elif "guide" in query:
            response = "🧭 Local guides can enhance your experience! Try contacting the place authorities for details."
        elif "map" in query or "location" in query:
            response = "🗺️ You can use the interactive map feature to view locations and navigate."
        elif "contact" in query or "reach" in query:
            response = "📞 Reach us through the contact section at the bottom of the page."
        elif "timing" in query or "open" in query:
            response = "⏰ Timings vary by location. Check the specific place details for accurate information."
        elif "hello" in query or "hi" in query or "hey" in query:
            response = "Hi there! 👋 Ask me anything about cultural heritage, places, or tips!"
        else:
            response = "🤖 I'm still learning! Try asking about festivals, food, heritage sites, maps, or etiquette."

    return render(request, 'heritage/chatbot.html', {'response': response})


def calendar_view(request):
    places = Place.objects.all()
    return render(request, 'heritage/calendar.html', {'places': places})

def donate(request):
    return render(request, 'heritage/donate.html')


def place_detail(request, slug):
    # Static dictionary of places with details
    places = {
        'taj-mahal': {
            'title': 'Taj Mahal',
            'location': 'Agra, Uttar Pradesh',
            'description': 'The Taj Mahal is a white marble mausoleum built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal. It’s one of the New Seven Wonders of the World and a UNESCO World Heritage Site.',
            'image': 'heritage/images/tajmahal.jpg'
        },
        'himalayas': {
            'title': 'The Himalayas',
            'location': 'Northern India',
            'description': 'The Himalayas are the highest mountain range in the world, offering breathtaking views, spiritual journeys, and thrilling treks across Himachal, Uttarakhand, and beyond.',
            'image': 'heritage/images/himalayas.jpg'
        },
        'ganga': {
            'title': 'Ganga Ghats',
            'location': 'Varanasi, Uttar Pradesh',
            'description': 'The Ganga Ghats of Varanasi are a sacred and spiritual destination for pilgrims. They offer mesmerizing views of the river, daily Ganga Aarti, and a deep connection with Indian traditions.',
            'image': 'heritage/images/ganga.jpg'
        },
        'goa': {
            'title': 'Goa Beaches',
            'location': 'Goa',
            'description': 'Goa is known for its pristine beaches, Portuguese architecture, seafood, and vibrant nightlife. It is a perfect mix of cultural heritage and modern holiday fun.',
            'image': 'heritage/images/goa.jpg'
        },
        'rishikesh': {
            'title': 'Rishikesh',
            'location': 'Uttarakhand',
            'description': 'Rishikesh, the Yoga Capital of the World, is located beside the Ganges river and is popular for meditation, white-water rafting, and spiritual experiences.',
            'image': 'heritage/images/rishikesh.jpg'
        },
        'india-gate': {
            'title': 'India Gate',
            'location': 'Delhi',
            'description': 'India Gate is a war memorial located in the heart of New Delhi. It commemorates the soldiers of the Indian Army who died in World War I and serves as a popular tourist spot.',
            'image': 'heritage/images/indiagate.jpg'
        },
    }

    place = places.get(slug)
    if not place:
        return render(request, 'heritage/404.html', status=404)

    return render(request, 'heritage/place_detail.html', {'place': place})

def hidden_gems(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    
    gems = HiddenGem.objects.all()
    if state:
        gems = gems.filter(state__iexact=state)
    if district:
        gems = gems.filter(district__iexact=district)

    return render(request, 'heritage/hidden_gems.html', {'gems': gems})

def hidden_gems_view(request):
    return render(request, 'hidden_gems.html')

from .forms import HiddenGemForm
from django.contrib import messages
from django.shortcuts import redirect

def submit_hidden_gem(request):
    if request.method == 'POST':
        form = HiddenGemForm(request.POST)
        if form.is_valid():
            gem = form.save(commit=False)
            gem.approved = False  # Require admin approval
            gem.save()
            messages.success(request, 'Your submission was received! Pending approval.')
            return redirect('submit_hidden_gem')
    else:
        form = HiddenGemForm()
    
    return render(request, 'heritage/submit_hidden_gem.html', {'form': form})

def hidden_gems(request):
    gems = HiddenGem.objects.filter(approved=True)
    return render(request, 'heritage/hidden_gems.html', {'gems': gems})




