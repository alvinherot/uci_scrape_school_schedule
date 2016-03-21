from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

def main():
    uci_school_url = 'https://www.reg.uci.edu/perl/WebSoc' 

    # Open url and store response
    scrape_response = urllib.request.urlopen(uci_school_url)

    # Convert response into a string
    scrape_resp_string = scrape_response.read()

    # Convert string into BeautifulSoup so we can use methods.
    html_bs4 = BeautifulSoup(scrape_resp_string, 'html.parser')

    # Find all "default" values for the form
    selected_forms = html_bs4.find_all('option', selected="selected")

    # Setup "default arguments" for form submission
    values = dict()
    for selected in selected_forms:
        values[selected.parent['name']] = selected['value']

    # Add specific values  that we actually watn to query.
    values["Dept"] = "COMPSCI"
    values["Submit"] = "Display Text Results"

    
    # All courses with {"major name" : "form input"}
    course_options = dict()

    # Scrape possible dept values
    dept_selections_scraped = html_bs4.find('select', attrs={"name":"Dept"})

    # dept_selections_scraped is a navigable string. Must perform find_all search on it
    # get the option tags, and then we cna access attributes
    for d in dept_selections_scraped.find_all('option'):
        course_name = d.string.split('.')[-1]
        course_options[course_name] = d['value']

    # Uncomment to see what the dict holds
    # print(values)
    # print()
    # print(course_options)
    
    # An example of what it should look like hardcoded.
    # values = {
            # 'YearTerm': '',
            # 'Breadth' : 'ANY',
            # 'Division': 'ANY',
            # 'Dept' : 'COMPSCI',
            # 'ClassType': 'ALL',
            # 'StartTime': '',
            # 'EndTime' : '',
            # 'FullCourses': 'ANY',
            # 'CancelledCourses' : 'Exclude',
            # 'Submit': 'Display Text Results'
            # }

    # Converts dictionary to iterable encoded string
    data = urllib.parse.urlencode(values)

    # We need to convery encoded strings to encoded binary
    # Open the request with url and data to send
    response = urllib.request.urlopen(uci_school_url, data.encode('utf8'))

    # Read response and store into content.
    content = response.read()

    # Decode binary to ascii
    for line in content.decode('ascii').split('\n'):
        print(line)





if __name__ == "__main__":
   main();
