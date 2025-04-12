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

from django.shortcuts import render

def chatbot_view(request):
    response = "Hello! How can I assist you today?"  # Default response

    # Expanded district-specific data for more locations across India
    district_data = {
        # Karnataka
        "bengaluru": {
            "title": "🏙 Bengaluru, Karnataka",
            "description": "Bengaluru, also known as Bangalore, is the tech capital of India. It’s famous for its startup ecosystem, vibrant culture, gardens like Lalbagh, and historical sites like Bangalore Palace."
        },
        "mysore": {
            "title": "🏰 Mysore, Karnataka",
            "description": "Mysore is known for the Mysore Palace, Chamundi Hill, and its rich cultural heritage. The city is also famous for its silk sarees and sandalwood products."
        },
        "hubli": {
            "title": "🏙 Hubli, Karnataka",
            "description": "Hubli is known for its thriving economy, historical sites like the Bhavanishankar Temple, and its proximity to the tranquil city of Dharwad."
        },
        "coorg": {
            "title": "🌿 Coorg, Karnataka",
            "description": "Coorg is famous for its coffee plantations, lush green landscapes, and scenic spots like Abbey Falls and Dubare Elephant Camp."
        },
        # Uttar Pradesh
        "varanasi": {
            "title": "🌊 Varanasi, Uttar Pradesh",
            "description": "Varanasi, also known as Kashi, is one of the oldest living cities in the world. It is a spiritual hub, famous for the ghats along the Ganges, Ganga Aarti, and temples like Kashi Vishwanath."
        },
        "lucknow": {
            "title": "🏙 Lucknow, Uttar Pradesh",
            "description": "Lucknow is famous for its Mughal-era monuments, including the Bara Imambara, and its rich culinary heritage, such as Tunday Kebab."
        },
        "agra": {
            "title": "🏰 Agra, Uttar Pradesh",
            "description": "Agra is home to the iconic Taj Mahal, one of the Seven Wonders of the World, as well as the Agra Fort and Fatehpur Sikri."
        },
        "kanpur": {
            "title": "🏙 Kanpur, Uttar Pradesh",
            "description": "Kanpur is a major industrial city, known for its textile industry and historical landmarks like the Kanpur Memorial Church."
        },
        # Goa
        "panaji": {
            "title": "🏖 Panaji, Goa",
            "description": "Panaji, the capital of Goa, is known for its vibrant Portuguese architecture, serene Mandovi River, and the Basilica of Bom Jesus."
        },
        "margao": {
            "title": "🏝 Margao, Goa",
            "description": "Margao is the commercial and cultural hub of South Goa, famous for its historical churches and proximity to stunning beaches like Colva."
        },
        "calangute": {
            "title": "🏖 Calangute, Goa",
            "description": "Calangute is one of the most popular beaches in Goa, known for its golden sands, vibrant nightlife, and water sports activities."
        },
        # Rajasthan
        "jaipur": {
            "title": "🏰 Jaipur, Rajasthan",
            "description": "Jaipur, the Pink City, is renowned for its palaces, forts, and vibrant bazaars. The Amber Fort, Hawa Mahal, and City Palace are must-visit landmarks."
        },
        "udaipur": {
            "title": "🏞 Udaipur, Rajasthan",
            "description": "Udaipur, often called the Venice of the East, is famous for its picturesque lakes, palaces like the City Palace, and its beautiful surroundings, making it a popular honeymoon destination."
        },
        "jodhpur": {
            "title": "🏰 Jodhpur, Rajasthan",
            "description": "Jodhpur, known as the Blue City, is famous for the Mehrangarh Fort, Umaid Bhawan Palace, and vibrant blue-painted houses."
        },
        "jaisalmer": {
            "title": "🏜 Jaisalmer, Rajasthan",
            "description": "Jaisalmer is known for its golden-hued fort, camel rides in the Thar Desert, and the beautiful Jain temples within the Jaisalmer Fort."
        },
        # Tamil Nadu
        "chennai": {
            "title": "🏙 Chennai, Tamil Nadu",
            "description": "Chennai is the gateway to southern India, known for its rich cultural heritage, classical dance (Bharatanatyam), and temples like the Kapaleeshwarar Temple. It also boasts beautiful beaches such as Marina Beach."
        },
        "madurai": {
            "title": "🏰 Madurai, Tamil Nadu",
            "description": "Madurai is famous for the Meenakshi Temple, one of the most important pilgrimage sites in India, as well as its vibrant bazaars and historic sites."
        },
        "coimbatore": {
            "title": "🏙 Coimbatore, Tamil Nadu",
            "description": "Coimbatore, also known as the Manchester of South India, is famous for its textile industry, as well as the nearby hill stations like Ooty."
        },
        # Kerala
        "kochi": {
            "title": "⚓ Kochi, Kerala",
            "description": "Kochi is known for its maritime history, colonial architecture, and beautiful backwaters. It is famous for the Chinese Fishing Nets, Fort Kochi, and the Kerala Kathakali Centre."
        },
        "thiruvananthapuram": {
            "title": "🌴 Thiruvananthapuram, Kerala",
            "description": "Thiruvananthapuram, the capital of Kerala, is famous for the Sree Padmanabhaswamy Temple and its proximity to beautiful beaches and backwaters."
        },
        # Maharashtra
        "mumbai": {
            "title": "🏙 Mumbai, Maharashtra",
            "description": "Mumbai, the financial capital of India, is known for the Gateway of India, Marine Drive, Bollywood, and its iconic beaches."
        },
        "pune": {
            "title": "🏙 Pune, Maharashtra",
            "description": "Pune is known for its historical significance, including the Aga Khan Palace and Sinhagad Fort. It’s a major cultural center with a strong academic presence and vibrant nightlife."
        },
        "nagpur": {
            "title": "🏙 Nagpur, Maharashtra",
            "description": "Nagpur, the Orange City, is famous for its vibrant markets and landmarks like the Deekshabhoomi, a significant Buddhist monument."
        },
        # Gujarat
        "ahmedabad": {
            "title": "🏙 Ahmedabad, Gujarat",
            "description": "Ahmedabad is known for its rich history, including the Sabarmati Ashram and the stunning architecture of the Sidi Saiyyed Mosque. It’s also famous for its textile industry and vibrant festivals like Navratri."
        },
        "surat": {
            "title": "🏙 Surat, Gujarat",
            "description": "Surat is known for its textile industry, diamond cutting, and vibrant cultural heritage, including the Dumas Beach and Surat Castle."
        },
        "vadodara": {
            "title": "🏙 Vadodara, Gujarat",
            "description": "Vadodara is known for the Laxmi Vilas Palace, the Baroda Museum, and its rich cultural traditions."
        },
        # Madhya Pradesh
        "bhopal": {
            "title": "🏙 Bhopal, Madhya Pradesh",
            "description": "Bhopal, the City of Lakes, is known for its historic architecture, beautiful lakes, and the UNESCO-listed Sanchi Stupa. It’s also home to the Bharat Bhavan cultural center."
        },
        "indore": {
            "title": "🏙 Indore, Madhya Pradesh",
            "description": "Indore is a prominent business and educational hub, known for its Indore Rajwada and Lal Baag Palace. The city is also famous for its street food, particularly Poha and Jalebi."
        },
        "gwalior": {
            "title": "🏰 Gwalior, Madhya Pradesh",
            "description": "Gwalior is known for its grand Gwalior Fort, one of the largest in India, and the stunning Saas-Bahu Temples."
        },
        # West Bengal
        "kolkata": {
            "title": "🏙 Kolkata, West Bengal",
            "description": "Kolkata, formerly Calcutta, is known for its colonial architecture, cultural festivals, and the iconic Howrah Bridge. It’s a cultural hub with sites like the Victoria Memorial and Indian Museum."
        },
        "darjeeling": {
            "title": "🏞 Darjeeling, West Bengal",
            "description": "Darjeeling is famous for its tea gardens, the Toy Train (a UNESCO World Heritage site), and stunning views of Mount Kanchenjunga."
        },
        "siliguri": {
            "title": "🏙 Siliguri, West Bengal",
            "description": "Siliguri is the gateway to North East India, known for its tea industry, and its proximity to the Himalayan range."
        },
        # Additional states (with prominent places)
        "delhi": {
            "title": "🏙 Delhi",
            "description": "Delhi, the national capital, is a blend of ancient and modern India. It is home to historical sites like the Red Fort, India Gate, and Qutub Minar, alongside bustling markets and modern infrastructure."
        },
        "bengaluru": {
            "title": "🏙 Bengaluru, Karnataka",
            "description": "Bengaluru, also known as Bangalore, is the tech capital of India. It’s famous for its startup ecosystem, vibrant culture, gardens like Lalbagh, and historical sites like Bangalore Palace."
        }
    }

    if request.method == 'POST':
        query = request.POST.get('query', '').lower()

        if "festival" in query or "event" in query:
            response = "🎉 You can check the Cultural Calendar page for upcoming festivals and events!"
        elif "respect" in query or "etiquette" in query:
            response = "🙏 Always respect local customs. Remove footwear at sacred places and dress modestly."
        elif "donate" in query or "support" in query:
            response = "💝 You can contribute to heritage preservation via the Donate page on our website."
        elif "heritage" in query or "culture" in query:
            response = "🌍 India has a rich cultural heritage! Explore our map and hidden gems itinerary to learn more."
        elif "food" in query or "cuisine" in query:
            response = "🍛 Don't miss local cuisines like Bisi Bele Bath in Karnataka or Dhokla in Gujarat!"
        elif "hello" in query or "hi" in query or "hey" in query:
            response = "Hi there! 👋 Ask me anything about cultural heritage, places, or tips!"
        else:
            # Check if query matches any district name
            for district, data in district_data.items():
                if district in query:
                    response = f"{data['title']}: {data['description']}"
                    break
            else:
                response = "🤖 I'm still learning! Try asking about festivals, food, heritage sites, maps, or etiquette."

    return render(request, 'heritage/chatbot.html', {'response': response})


def calendar_view(request):
    return render(request, 'heritage/calendar.html')

#def calendar_view(request):
   # places = Place.objects.all()
    #return render(request, 'heritage/calendar.html', {'places': places})

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

#from .forms import HiddenGemForm
#from django.contrib import messages
#from django.shortcuts import redirect

#def submit_hidden_gem(request):
    #if request.method == 'POST':
        #form = HiddenGemForm(request.POST)
        #if form.is_valid():
            #gem = form.save(commit=False)
            #gem.approved = False  # Require admin approval
            #gem.save()
            #messages.success(request, 'Your submission was received! Pending approval.')
            #return redirect('submit_hidden_gem')
    #else:
        #form = HiddenGemForm()
    
    #return render(request, 'heritage/submit_hidden_gem.html', {'form': form})

#def hidden_gems(request):
    #gems = HiddenGem.objects.filter(approved=True)
    #return render(request, 'heritage/hidden_gems.html', {'gems': gems})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import HiddenGemForm
from .models import HiddenGem

# View for filtering and listing gems
def filtered_hidden_gems(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    
    gems = HiddenGem.objects.all()
    if state:
        gems = gems.filter(state__iexact=state)
    if district:
        gems = gems.filter(district__iexact=district)

    return render(request, 'heritage/hidden_gems.html', {'gems': gems})

# View for submitting a new hidden gem
def submit_hidden_gem(request):
    if request.method == 'POST':
        form = HiddenGemForm(request.POST)
        if form.is_valid():
            gem = form.save(commit=False)
            gem.approved = False  # Require admin approval
            gem.save()
            messages.success(request, 'Your submission was received! Pending approval.')
            return redirect('submit_hidden_gem')  # Ensure this URL is correctly mapped in your urls.py
    else:
        form = HiddenGemForm()
    
    return render(request, 'heritage/submit_hidden_gem.html', {'form': form})

# View for listing approved gems
def approved_hidden_gems(request):
    gems = HiddenGem.objects.filter(approved=True)
    return render(request, 'heritage/hidden_gems.html', {'gems': gems})




