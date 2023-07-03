import requests
import concurrent.futures

def download_pdf(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"PDF file downloaded successfully: {file_path}")
    else:
        print(f"Failed to download the PDF file: {url}")

# Read URLs from file
file_path = 'tr_did_values.txt'  # Replace with the path to your file containing URLs
with open(file_path, 'r') as file:
    urls = file.read().splitlines()

# Download PDF files concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for i, url in enumerate(urls):
        text = url.replace("https://www.centralbankbahamas.com/viewPDF/documents/","")
        text = text.replace(".pdf","")
        pdf_file_path = f'data/400.491/{text}.pdf'  # Replace with the desired file path for each PDF
        future = executor.submit(download_pdf, url, pdf_file_path)
        futures.append(future)

    # Wait for all futures to complete
    concurrent.futures.wait(futures)

print("All PDF files downloaded successfully.")
