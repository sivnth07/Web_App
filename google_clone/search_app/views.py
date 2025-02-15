from django.shortcuts import render
from django.http import HttpResponse
from googlesearch import search  # For performing the search
import requests  # For fetching metadata from search result pages
from bs4 import BeautifulSoup  # For parsing HTML content
from .models import SearchQuery


def fetch_metadata(url):
    """Fetch the title and description of a web page."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title and meta description
        title = soup.title.string if soup.title else url
        description_meta = soup.find('meta', attrs={'name': 'description'})
        description = description_meta['content'] if description_meta else "No description available."
        
        return {'title': title, 'description': description, 'url': url}
    except Exception as e:
        print(f"Error fetching metadata for {url}: {e}")
        return {'title': url, 'description': "Could not retrieve details.", 'url': url}


def home(request):
    if request.method == 'POST':
        query = request.POST.get('search_query', '')  # Get the search query
        if query:
            # Save the search query to the database with a timestamp
            SearchQuery.objects.create(query=query)
            
            # Fetch search results
            search_results = []
            try:
                urls = search(query, num_results=10)  # Fetch 10 search result URLs
                for url in urls:
                    metadata = fetch_metadata(url)  # Fetch title and description
                    search_results.append(metadata)
            except Exception as e:
                print(f"Error fetching search results: {e}")
            
            # Pass the query and search results to the results template
            return render(request, 'search_app/results.html', {'query': query, 'results': search_results})
    
    return render(request, 'search_app/home.html')