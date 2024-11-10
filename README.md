# Web Scraping Project for Product, Service, and Founder Information

This project outputs “Products,” “Services,” and “Founder(s)” data for each of the specified domains, leveraging BeautifulSoup, ScrapeGraphAI, and OpenAI for a multi-step information extraction process.

## Project Overview

The purpose of this script is to automatically scrape structured information about each company's offerings (products/services) and founder details from their website. Specifically, we target and extract:

- Products: Unique products offered by the company
- Services: Services provided by the company
- Founder(s): Names of the Founders

The code uses a combination of web scraping techniques (with BeautifulSoup), intelligent parsing (ScrapeGraphAI and OpenAI), and regex-based text extraction to create structured data outputs into the console.

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Dependencies](#dependencies)
4. [How It Works](#how-it-works) 
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Output](#output)
8. [Error Handling](#error-handling)
9. [Future Improvements](#future-improvements)
10. [Assessment Written Questions](#assessment-written-questions)

# Getting Started

To run this code, you'll need Python 3.12.4 installed and to set up the required dependencies.

## Dependencies
The following Python libraries are required:

- json (standard library) for handling JSON data
- requests for making HTTP requests
- BeautifulSoup from bs4 for parsing HTML
- ScrapeGraphAI (via the scrapegraphai library) for enhanced intelligent scraping
- OpenAI for interacting with GPT models to extract and process text information
- re (standard library) for regular expressions to locate and parse founder-related text

Install dependencies with:
            pip install requests beautifulsoup4 scrapegraphai openai

## How It Works

#### Workflow:
- API Setup: Sets up the OpenAI API key for natural language processing.
- Domain Scraping: Iterates over each domain to extract primary data from the main page and internal links.
- HTML Data Collection: The grab_website_data function fetches HTML content and parses it using BeautifulSoup.
- Internal Link Extraction: find_internal_links finds links within the same domain to gather additional relevant data from all website tabs.
- Data Consolidation: For each domain, extract_with_scrapegraph uses ScrapeGraphAI and OpenAI models to identify and extract specific pieces of information.
- Data Parsing and Filtering: Uses regex to identify and consolidate sentences mentioning founder roles. Filters text data to avoid irrelevant information.
- Output Generation: Outputs the “Products,” “Services,” and “Founder(s)” information for each domain, consolidating the final output for easy reading.

Functions Overview:

- grab_website_data: Retrieves the HTML content from a given URL.
- find_internal_links: Finds all internal links on a page for further data exploration.
- add_text_items: Consolidates textual data while filtering out non-string values.
- extract_founder_sentences: Uses regex to find sentences with founder-related keywords.
- extract_with_scrapegraph: Utilizes ScrapeGraphAI and OpenAI models to extract key information from specified web pages.

## Usage

Set OpenAI API Key: Replace "xxx" with your OpenAI API key:

        client = openai.OpenAI(api_key="xxx")

If the code outputs: 

        "Error processing <domain>: list index out of range"

You may need to start a new project in your OpenAI account and create new project-associated API keys to run the code. 

Run the script: Run the main function to process each domain and output the structured data for each.
python web_scraping_project.py

## Configuration

The configuration section defines the setup for ScrapeGraphAI. Key elements include:

- llm: Uses OpenAI’s GPT model to process and understand web content.
- verbose: Prints detailed information about the scraping process, aiding in debugging and monitoring. Set to "False" if extra information isn't desired.

## Output

For each domain, the output is organized as follows:

            Final consolidated data for <domain>:
            Products: [List of Products]
            Services: [List of Services]
            Founders: [List of Founder Name(s)]

The output is filtered to include only items of sufficient length and relevance, making it concise and structured.

## Error Handling

- Connection Errors: grab_website_data handles HTTP connection errors gracefully.
- ScrapeGraphAI Errors: If data extraction fails, an error message will display without stopping the entire script.
- Data Validation: Checks if returned data is empty and prints an alert if ScrapeGraphAI returns no data.

## Future Improvements

Potential areas for enhancement include:

- Dynamic Domain List: Adding an option for users to input custom domains dynamically.
- Enhanced Founder Detection: Improving the regex patterns or using NLP techniques for more nuanced sentence analysis.
- Additional Data Types: Extending to extract data such as funding rounds, locations, or company mission statements.

In particular, the following could be improved to further streamline and clean up our script outputs:

1. Distinguishing Products from Services:

To improve the accuracy of our data categorization, we plan to implement AI-driven filtering to distinguish between "products" and "services" in the output more effectively. Currently, some product and service names are duplicated or miscategorized, leading to confusion in the output. We propose using spaCy for this task, leveraging its Named Entity Recognition (NER) capabilities to attempt to classify items based on keywords and context clues. Specifically, we can use the following prompts to guide spaCy’s filtering:

- Products Prompt: “List only physical or digital products, excluding any consulting or support actions.” 

Products typically include terms like “software,” “tool,” “app,” or “platform,” which spaCy can use as indicators.

- Services Prompt: “List only actions or support offerings, excluding any tangible or digital items.”
    
Services usually include terms like “consulting,” “monitoring,” “support,” or “management,” which will help spaCy identify them correctly.

By using these prompts and spaCy’s NER model, we can create a robust system for classifying items, removing duplicates, and ensuring that only unique values are included in each category.

2. Validation of Key Data (e.g., Founder Names):

For further data validation, particularly for key personnel like founders, we plan to use a second AI-driven approach. Here, spaCy or a similar tool could automate verification by searching the internet for specific queries, such as “company name/domain name” + “Founder.” By retrieving and parsing search results, Deepchecks NLP can potenitally help, identifying relevant names and titles, which we can then compare with our dataset to verify accuracy. A text similarity metric (such as cosine similarity on text embeddings) can be applied to ensure high confidence in matching names. This process will allow for automated, reliable validation of sensitive information.

3. Obtaining data from Website Images:

To further enhance this process, since many images on the site contain valuable information that ScrapeGraph AI cannot interpret, we propose adding an AI tool with Optical Character Recognition (OCR) capabilities, potentially Google Cloud AI. OCR would allow us to extract text from images, consolidating this data with the information obtained through web scraping, thus ensuring we capture all relevant data for analysis. Integrating OCR with ScrapeGraph AI and OpenAI would create a more comprehensive data-gathering process, enabling better insights and a cleaner model output.

The above are just some of the ways in which we could improve the performance of our model and clean up our model output.

## Assessment Written Questions

1. Why did we at Sequel build https://www.pitchleague.ai? What is our goal for this website? How would you improve this product?

Pitch League was created to help startups gain visibility and improve performance by offering targeted advice and driving more traffic to their platforms. Since Sequel connects athletes with investment opportunities in startups, it would be beneficial for Sequel to offer a platform where athletes can explore various startups and identify business sectors they might want to invest in. The platform is thoughtfully organized, allowing users to easily browse through startups, view business descriptions, and understand the products and services offered. Additionally, it provides a score for different business aspects, along with an overall rating, which serves as a useful starting point for athletes, general investors, and the public alike.

To enhance the user experience, we could consider adding a search feature that allows users to find startups based on specific keywords related to their interests. This would make it easier for potential investors to discover startups that align with their goals or to find particular products and services. This feature could increase website traffic by enabling users to customize their search experience. Additionally, implementing personalized recommendations — such as “Because you viewed these companies or searched for these terms, you might like these startups” — would encourage users to stay engaged and explore related companies that may also spark their interest.

Moreover, adding transparency around the scoring system by including the criteria for each category could help users better understand how each company is evaluated, enhancing the credibility and value of the ratings.

2. How can we combine information from pitch decks and crawling websites?

To create a comprehensive profile of each company, we can integrate structured information from pitch decks with real-time data from their websites. Using various NLPs, we can extract key elements from pitch decks, such as mission, product descriptions, target audience, and financial metrics. For decks in image format, OCR tools, like the previously mentioned Google Cloud AI, convert images to text before NLP processing. Simultaneously, web scraping can gather real-time data from company websites, including details on products and services, team bios, recent news, and testimonials. If available, API access can provide more structured data than traditional scraping.

Once data is collected from both sources, we can use AI models to classify information into categories like “Products,” “Services,” “Team,” and “Financials,” (as we did in this project), helping to differentiate offerings by identifying terms associated with products (e.g., "platform" or "software") and services (e.g., "consulting" or "support"). Any overlapping information would be consolidated to ensure unique entries. Using cross-referencing techniques, we can use various NLPs (like the afforementioned Deepchecks) to validate similar data points between pitch decks and websites, such as verifying the CEO’s name or matching financial figures, with text similarity models highlighting related content. Any inconsistencies between the two sources would be flagged for further investigation. Finally, insights from the pitch deck can be enriched with live website data, producing a unified profile that reflects both the strategic goals outlined in the pitch and the current operational status of the company. This combined approach offers investors and analysts a well-rounded, up-to-date understanding of each company.