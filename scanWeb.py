import requests
from bs4 import BeautifulSoup
from xleSave import saveToXle,count_data_entries

class dc_scaning():
    
    def __init__(self, url):
        self.url = url
        self.scan_records = []

    def update_url(self, new_url):
        self.url = new_url

    def scan_activated(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
        else:
            print('Failed to retrieve data from the website')

    def main_scan(self):
            selected_div = self.soup.find('div', class_='tab-content left-tab-1 selected')
            if selected_div:
                a_elements = selected_div.find_all('a', class_='img')
                href_list = []
                time_list = []
                title_list = []
                type_list = []
                ep_list = []
            for a in a_elements:
                href = a['href']
                span_time = a.find('span', class_='time').text
                h3_title = a.find('h3', class_='title').text
                # Extract the type and episode spans
                span_type = a.find('span', class_='type RAW') or a.find('span', class_='type SUB')
                span_ep = a.find('span', class_='ep RAW') or a.find('span', class_='ep SUB')
                # If the spans are found, extract their text, otherwise, set to None
                type_text = span_type.text if span_type else None
                ep_text = span_ep.text if span_ep else None

                href_list.append(href)
                time_list.append(span_time)
                title_list.append(h3_title)
                type_list.append(type_text)
                ep_list.append(ep_text)
                # the final data
                data = {
                'href': href_list,
                'Time': time_list,
                'Title': title_list,
                'Type': type_list,
                'Episode': ep_list
                }
            # excel sheet stroge
            sheet = 'dcd.xlsx'
            saveToXle(data,sheet)
            print(f"Number of data entries (excluding index): {count_data_entries(sheet)}")
            self.add_scan_record('main_scan')
        

    def view_more(self):
            view_more_link = self.soup.find('div', class_='view-more')
            if view_more_link:
                view_more_url = view_more_link.find('a')['href']
                print("Continuing to next page:", view_more_url)
                self.update_url(view_more_url)
                self.scan_activated()
                self.add_scan_record('view_more')
                
    def get_more_pages(self):
        print('get on')
        base_url = self.url.split('?')[0]  # Extract base URL without parameters
        current_page = 1
        pg = 5
        while current_page <= 365:
            print('while work')
            next_50_pages = range(current_page, min(current_page + pg, 365))  # Determine the range of next 50 pages

            for page_num in next_50_pages:
                next_page_url = f"{base_url}?page={page_num}"  # Construct URL for next page
                print("Scanning page:", next_page_url)
                self.update_url(next_page_url)
                self.scan_activated()
                self.main_scan()
                self.add_scan_record('get_more_pages')

            # Prompt the user to continue scanning the next set of 50 pages
            if current_page + pg <= 365:
                choice = input(f"Do you want to scan the next set of {pg} pages? (y/n): ").lower()
                if choice == 'n':
                    break  # If user does not want to continue, break the loop

            current_page += pg
    
    def add_scan_record(self, function_name):
        import datetime
        timestamp = datetime.datetime.now().strftime('%I:%M%p %d.%m.%Y')
        self.scan_records.append({
            'Time': timestamp,
            'Function Performed': function_name,
            'URL': self.url
        })

    def create_scan_record_file(self):
        with open('scan_record.txt', 'w') as file:
            file.write('# | Time                  | Function Performed | URL\n')
            for i, record in enumerate(self.scan_records, start=1):
                file.write(f"{i} | {record['Time']} | {record['Function Performed']: <20} | {record['URL']}\n")


if __name__ == "__main__":
    url = 'https://example.com/'

    scanner = dc_scaning(url)
    scanner.scan_activated()

    # Initial scan
    scanner.main_scan()

    # Prompt user for further action
    while True:
        choice = input("Do you want to continue scanning? (Y/N): ").strip().lower()
        if choice != 'y':
            break

        # Ask if user wants to continue with "View more" or pagination links
        action = input("Do you want to continue with 'view_more' or 'pagination'? ").strip().lower()

        if action == 'view_more' or action == 'vm':
            scanner.view_more()
        elif action == 'pagination'or action == 'pg':
            print('paging......')
            scanner.get_more_pages()
        else:
            print("Invalid option! Please enter 'view_more' or 'pagination'.")

    # Create the scan record file
    scanner.create_scan_record_file()
