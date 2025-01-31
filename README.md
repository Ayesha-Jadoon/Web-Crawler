# Simple Web Crawler

A Python-based web crawler designed to perform efficient, breadth-first traversal of websites. This crawler extracts relevant content such as links, titles, headings, paragraphs, and images from webpages, stores the collected data in a structured JSON format, and respects `robots.txt` to ensure ethical crawling. It uses concurrent threads to speed up the crawling process while avoiding duplicates by leveraging hashing techniques.

## Features
- **Breadth-First Search (BFS)**: Uses BFS for traversing the website, ensuring that the crawler explores a webpage and all of its links within a specified depth before moving on to the next level of links.
- **Content Extraction**: Extracts key information including the page title, headings, paragraphs, and image sources, which are crucial for various types of web scraping and data analysis projects.
- **Duplicate Detection**: Implements SHA-256 hashing to generate unique identifiers for page content, allowing the crawler to skip pages with duplicate content and optimize the crawling process.
- **Respect for robots.txt**: Ensures compliance with the website’s crawling policies by checking the `robots.txt` file before accessing any URL. If crawling is not allowed for a page, the crawler will skip it.
- **Multithreading**: Uses Python’s `ThreadPoolExecutor` for concurrent fetching of pages, improving the overall performance and speed of the crawler.
- **Data Saving**: The extracted content is saved in a JSON file, providing an easy-to-read and portable format for further analysis or storage.

## Data Structures and Algorithms (DSA) Concepts Used
- **Queue (BFS)**: Implements a queue to store URLs in a breadth-first manner, ensuring that the crawler processes each page before moving on to linked pages.
- **Set**: Utilizes sets to track visited URLs and hashed page contents, preventing the crawler from revisiting the same pages and ensuring that no duplicate content is processed.
- **Hashing**: Generates SHA-256 hashes for page content to uniquely identify and detect duplicate pages, skipping them if already encountered.
- **Threading**: Makes use of multithreading to fetch pages concurrently, enhancing the crawler’s speed and efficiency, especially for large websites with numerous pages.

## Tested Websites
- http://quotes.toscrape.com/
- http://books.toscrape.com/
- http://commoncrawl.org.com/
- www.google.com
- https://www.daraz.pk/


## Screenshots

The output screenshots of the tested websites are available in the [Output.pdf](https://github.com/Ayesha-Jadoon/Web-Crawler/blob/main/Output.pdf) file.


## Requirements
- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation and Usage

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/your-username/Simple-Web-Crawler.git
    ```

2. Install the required dependencies using `pip`:
    ```bash
    pip install requests beautifulsoup4
    ```

3. Run the crawler:
    ```bash
    python main.py
    ```

4. Enter the website URL when prompted for crawling.

## Output

- The crawler will save the extracted data in a JSON file within the `output` folder. The filename will be based on the domain name of the website, such as:
  
    ```bash
    output/example.com_crawled_data.json
    ```

- The JSON file will contain a list of crawled pages with their content, including:

    - `url`: The URL of the crawled page
    - `title`: The title of the page
    - `headings`: A list of headings (h1 to h6) found on the page
    - `paragraphs`: A list of paragraphs from the page
    - `images`: A list of image sources found on the page

