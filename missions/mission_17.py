import requests
import os
import json
import html2text
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
from core.send_response import send_response
from core.openai_functions import generate_answer

def get_questions():
    """
    Fetches questions from API and saves them to a JSON file.
    Returns a dictionary of questions.
    """
    softo_questions = requests.get(os.getenv("SOFTO_QUESTIONS"))
    os.makedirs('media/softo', exist_ok=True)
    with open('media/softo/questions.json', 'w', encoding='utf-8') as f:
        json.dump(softo_questions.json(), f, ensure_ascii=False)
    
    return softo_questions.json()

def get_visible_links(soup):
    """
    Extracts visible links from BeautifulSoup object after removing hidden elements.
    Returns a list of link URLs.
    """
    # Remove hidden elements
    for hidden in soup.find_all(attrs={'hidden': True}):
        hidden.decompose()
    return [a.get('href') for a in soup.find_all('a') if a.get('href')]

def get_whole_site(start_url, visited=None):
    """
    Extracts visible links from BeautifulSoup object after removing hidden elements.
    Returns a list of link URLs.
    """
    # Remove hidden elements
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for hidden in soup.find_all(attrs={'hidden': True}):
        hidden.decompose()
    return [a.get('href') for a in soup.find_all('a') if a.get('href')]


def clean_and_parse_page(response):
    """
    Cleans page content by removing hidden elements and scripts,
    then converts to markdown.
    Returns BeautifulSoup object and markdown content.
    """
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove hidden elements, head, scripts
    for hidden in soup.find_all(attrs={'hidden': True}):
        hidden.decompose()
    for tag in soup.find_all(['head', 'script']):
        tag.decompose()
        
    markdown_content = html2text.html2text(str(soup))
    return soup, markdown_content

def check_for_answer(content, question):
    """
    Uses GPT to check if content contains answer to question.
    Returns tuple of (has_answer, answer_text).
    """
    check_prompt = [
        {"role": "system", "content": "You are a precise answer detector. Assess whether the content answers a specific question. Respond only with YES or NO."},
        {"role": "user", "content": f"Does this content contain a direct answer to: {question}\n\nContent: {content}"}
    ]
    
    has_answer = generate_answer("gpt-4o-mini", check_prompt)
    
    if has_answer == "YES":
        extract_prompt = [
            {"role": "system", "content": "Extract the exact answer. Be concise and specific. No explanations."},
            {"role": "user", "content": f"What is the answer to: {question}\n\nContent: {content}"}
        ]
        answer = generate_answer("gpt-4o-mini", extract_prompt)
        return True, answer
        
    return False, None

def mission_17():
    """
    Main function that:
    1. Fetches questions from API
    2. Crawls website to find answers
    3. Sends answers back via API
    
    The crawler follows links and uses GPT to detect and extract answers
    from page content.
    """
    questions = get_questions()
    
    base_url = "https://softo.ag3nts.org"
    answers = {}

    # Get initial links from homepage
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_links = get_visible_links(soup)
    print(all_links)

    # Process each question
    for question_id, question_text in questions.items():
        found_answer = False
        visited_urls = set()
        steps = 0
        max_steps = 20

        # Check all visible links
        for link in all_links:
            if found_answer or steps >= max_steps:
                break
                
            current_url = link if link.startswith('http') else base_url + link
            
            if current_url in visited_urls:
                continue
            visited_urls.add(current_url)
            steps += 1

            try:
                response = requests.get(current_url)
                soup, markdown_content = clean_and_parse_page(response)
                
                # Check if page contains answer
                has_answer, answer = check_for_answer(markdown_content, question_text)
                
                if has_answer:
                    answers[question_id] = answer
                    found_answer = True
                    print(f"Found answer in link for question {question_id}")

                # Add new links from this page
                new_links = get_visible_links(soup)
                all_links.extend([link for link in new_links if link not in all_links])

            except Exception as e:
                print(f"Error processing link {current_url}: {str(e)}")
                continue

        if not found_answer:
            print(f"Could not find answer for question {question_id} after {steps} steps")
            answers[question_id] = "Not found"

    # Send final answers
    response = send_response(os.getenv("RAPORT_URL"), "softo", answers)
    print("Response:", response)
