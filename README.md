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
- OpenAI for interacting with GPT models to extract and process text information (can use any of the models but we used "gpt-4o-mini")
- re (standard Python library) for regular expressions to locate and parse founder-related text

Install dependencies with:
            pip install requests beautifulsoup4 scrapegraphai openai

## How It Works

#### Workflow:
- API Setup: Sets up the OpenAI API key for natural language processing.
- Domain Scraping: Iterates over each domain to extract primary data from the main page and internal links.
- HTML Data Collection: The grab_website_data function fetches HTML content and parses it using BeautifulSoup.
- Internal Link Extraction: find_internal_links finds links within the same domain to gather additional relevant data from all website tabs.
- Data Consolidation: For each domain, scrape_website uses ScrapeGraphAI and OpenAI models to identify and extract specific pieces of information using a prompt(s).
- Data Parsing and Filtering: Uses regex to identify and consolidate sentences mentioning founder roles. Filters text data to avoid irrelevant information.
- Output Generation: Outputs the “Products,” “Services,” and “Founder(s)” information for each domain, consolidating the final output for easy reading.

#### Functions Overview:

- grab_website_data: Retrieves the HTML content from a given URL.
- find_internal_links: Finds all internal links on a page for further data exploration.
- add_text_items: Consolidates textual data while filtering out non-string values.
- extract_founder_sentences: Uses regex to find sentences with founder-related keywords.
- scrape_website: Utilizes ScrapeGraphAI and OpenAI models to extract key information from specified web pages.

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

To improve the accuracy of our data categorization, we plan to implement AI-driven filtering to distinguish between "products" and "services" in the output more effectively. Currently, some product and service names are in both sets or miscategorized, leading to confusion in the output. We propose using spaCy for this task, leveraging its Named Entity Recognition (NER) capabilities to attempt to classify items based on keywords and context clues. Specifically, we can use the following prompts to guide spaCy’s filtering:

- Products Prompt: “List only physical or digital products, excluding any consulting or support actions.” 

Products typically include terms like “software,” “tool,” “app,” or “platform,” which spaCy can use as indicators.

- Services Prompt: “List only actions or support offerings, excluding any tangible or digital items.”
    
Services usually include terms like “consulting,” “monitoring,” “support,” or “management,” which will help spaCy identify them correctly.

By using these prompts and spaCy’s NER model, we can create a robust system for classifying items, removing duplicates, and ensuring that only unique values are included in each category.

2. Validation of Key Data (e.g., Founder Names):

For further data validation, particularly for founder data, we plan to use a second AI-driven approach. Here, Deepchecks NLP, spaCy, or a similar tool could automate validation or verification by searching the internet for specific queries, such as “company name/domain name” + “Founder.” By retrieving and parsing search results, AI can help in identifying relevant names and titles, which we can then compare with our dataset to verify accuracy. A text similarity metric (such as cosine similarity on text embeddings) can be applied to ensure high confidence in matching names. This process will allow for automated, reliable validation of sensitive information, reducing manual verification effort and improving data integrity.

3. Obtaining data from Website Images:

To further enhance this process, since many images on the site contain valuable information that ScrapeGraph AI cannot interpret, we propose adding an AI tool with Optical Character Recognition (OCR) capabilities, potentially Google Cloud AI. OCR would allow us to extract text from images, consolidating this data with the information obtained through web scraping, thus ensuring we capture all relevant data for analysis. Integrating OCR with ScrapeGraph AI and OpenAI would create a more comprehensive data-gathering process, enabling better insights and a cleaner model output.

The above are just some of the ways in which we could improve the performance of our model and clean up our model output.
