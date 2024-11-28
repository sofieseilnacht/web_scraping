import json
import requests
from bs4 import BeautifulSoup
from scrapegraphai.graphs import SmartScraperGraph
import openai
import re

# Set up OpenAI API key
client = openai.OpenAI(key="")


# List of domain names to scrape
domains = [
    "https://tonestro.com/",
    "https://www.sendtrumpet.com/",
    "https://www.prewave.com/",
    "https://twinn.health/",
    "https://kokoon.io/"
]

# Configure ScrapeGraphAI with OpenAI API
# Found on the ScrapeGraphAI website as "Use Case 3"
graph_config = {
    "llm": {
        "api_key": client.api_key,
        # I used gpt-4o instead of "gpt-3.5-turbo" as I found that examples of that model working on StackOverflow
        "model": "openai/gpt-4o-mini",
    },
    # Get detailed logs of what is being scraped using scrapegraphai (can set to False if want less output in console)
    "verbose": True,
}

# Function to fetch HTML content from a URL (for preliminary checks)
# Found documentation for requests and Beautiful soup on DigitalOcean
# Use try/except code so we don't crash the script if any of the websites are down, and we can move onto the next domain without any issue
def grab_website_data(url):
    try:
        website = requests.get(url)
        website.raise_for_status()
        website_data = BeautifulSoup(website.text, 'html.parser')
        return website_data
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return None

# Function to find internal links on a webpage so we can scrape each page found for more data
def find_internal_links(html_data, base_url):
    # URLs don't need to be in a specific order and we don't want duplicates
    links = set()
    # Find all the "a" tags with associated with "href" attributes in the HTML to grab the hyperlinks on each page so we can add them to the list of URLs
    for link in html_data.find_all("a", href=True):
        href = link["href"]
        # "/" means the link is a relative link
        if href.startswith("/"):  
            links.add(base_url + href)
        # no "/" means the link is an absolute link
        elif base_url in href:  # Absolute link
            links.add(href)
    return links

# Helper function to add only string values to the consolidated data sets
def add_text_items(consolidated_set, items):
    for item in items:
        if isinstance(item, str):
            consolidated_set.add(item)
        # If item is a dictionary, extract its values (had the dictionary issue with kokoon.io)
        elif isinstance(item, dict):  
            for value in item.values():
                if isinstance(value, str):
                    consolidated_set.add(value)

# Function to extract sentences containing founder-related information using regex
def extract_founder_sentences(text):
    # No specific order for the presented founders
    founder_info = set()
    # Using regex to match titles and keywords
    pattern = r"\b(CEO|CTO|founder|founded)\b"  
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)  
    for sentence in sentences:
    # re.IGNORECASE makes the text not case sensitive so we can focus on letters themselves rather than if they're capitalized or not
        if re.search(pattern, sentence, re.IGNORECASE):
            founder_info.add(sentence.strip())
    return founder_info

# Still in "Use Case 3" on the ScrapeGraphAI Documentation
# Write a function to automate the search through all the domains
# Use try/except code for same reason as above
def scrape_website(url):
    try:
        smart_scraper_graph = SmartScraperGraph(
        # Prompt is fairly specific here, but can be tailored to be more or less specific depending on what we're looking for
            prompt="Extract the company's services, products, and Founder(s) name(s). For services and products, only include data written in the english language. In terms of the founder portion, look specifically for people whose role says at least founder. If the word founder isn't associated with it, don't include the person's name in the list of Founders. The word founder could be on top of images in the website, so you may need to associate the names of the people in the pictures with the word founder is it isnt explicitly stated. Make sure the founder is for the company domain, and not founder of a different company.",
            source=url,
            config=graph_config
        )

        # Run the scraping pipeline
        result = smart_scraper_graph.run()
        
        # Check if result is None or empty
        if result:
            # Adjusting to expect either strings or nested dictionaries here
            # Using a dictionary to organize data because we anticipate multiple keys with multiple values respectively (e.g., "products", "services", "founders").
            return {
                "products": result.get("products", []),
                "services": result.get("services", []),
                "founders": result.get("founders", []) 
            }
        else:
            print(f"No data returned by ScrapeGraphAI for {url}.")
            return None

    except IndexError as e:
        print(f"IndexError processing {url}: {e}")
    except Exception as e:
        print(f"General error processing {url}: {e}")
        return None

# Main function to automate looping through each domain and extract information
def main():
    for base_url in domains:
        print(f"\nProcessing {base_url}...")

        # Initialize consolidated data and a flag to track if founders are found
        # Using sets so we can make sure we don't include duplicate values (strings)
        consolidated_data = {
            "products": set(),
            "services": set(),
            "founders": set()
        }

        # Flag to check if any founders were found
        # Initialize founders_found to False because we are assuming we have no prior knowledge of whether the site contains founder information
        founders_found = False  

        # Grab the main page data and check internal links
        html_data = grab_website_data(base_url)
        if html_data:
            # Extract and print the page's meta description if available
            description = html_data.find("meta", attrs={"name": "description"})
            if description:
                print("Basic Description (from meta):", description["content"])
            
            # Grab the links of all the pages within the website so we can scrape for data 
            internal_links = find_internal_links(html_data, base_url)
            
            # Process main page
            result = scrape_website(base_url)
            if result:
                # Add any found products to the consolidated data's "products"  and "services" sets
                add_text_items(consolidated_data["products"], result["products"])
                add_text_items(consolidated_data["services"], result["services"])

                # Use helper function for founder-related sentences if founders aren't directly in result
                # Check if founders are present directly in the scrape result
                if result["founders"]:
                    add_text_items(consolidated_data["founders"], result["founders"])
                    founders_found = True
                # If no founders are directly found, search the page text for possible founder-related sentences
                else:
                    page_text = html_data.get_text()
                    founder_sentences = extract_founder_sentences(page_text)
                    # Add any extracted sentences mentioning founders to the consolidated data
                    consolidated_data["founders"].update(founder_sentences)
                    # Set the flag to True if any founder-related sentences were found
                    if founder_sentences:
                        founders_found = True
            
            # Process each internal link and accumulate results
            for link in internal_links:
                print(f"\nProcessing linked page: {link}")
                # Retrieve HTML data for the current linked page
                linked_html_data = grab_website_data(link)
                
                if linked_html_data:
                    # Extract and print the meta description if available
                    description = linked_html_data.find("meta", attrs={"name": "description"})
                    if description:
                        print("Basic Description (from meta):", description["content"])

                    # Scrape the linked page for specific data categories
                    result = scrape_website(link)
                    if result:
                        add_text_items(consolidated_data["products"], result["products"])
                        add_text_items(consolidated_data["services"], result["services"])
                        
                        if result["founders"]:
                            add_text_items(consolidated_data["founders"], result["founders"])
                            founders_found = True

                        # If no founders are found, search the page text for potential founder mentions
                        else:
                            page_text = linked_html_data.get_text()
                            founder_sentences = extract_founder_sentences(page_text)
                            consolidated_data["founders"].update(founder_sentences)
                            if founder_sentences:
                                founders_found = True

        if not founders_found:
            print("No founders found across pages for this domain.")

        # Filter each list to include only items with 3 or more characters before printing (had issues with random letters and white space popping up in the sets)
        products_filtered = [item for item in consolidated_data["products"] if len(item) >= 3 and len(item.split()) <= 8]
        services_filtered = [item for item in consolidated_data["services"] if len(item) >= 3 and len(item.split()) <= 8]
        # Want full names so not just first or last names, although can adjust if first names work just as well
        founders_filtered = [item for item in consolidated_data["founders"] if len(item.split()) >= 2]

        # Print consolidated and filtered data for the domain
        print(f"\nFinal consolidated data for {base_url}:")
        print("Products:", ", ".join(products_filtered))
        print("Services:", ", ".join(services_filtered))
        print("Founders:", " | ".join(founders_filtered))  # Using separator for better readability

if __name__ == "__main__":
    main()
