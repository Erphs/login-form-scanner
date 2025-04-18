import requests
from bs4 import BeautifulSoup
from termcolor import colored  # For using colors in terminal


# This function is used to find login forms on a webpage
def find_login_forms(url):
    try:
        # Sending a GET request to the provided URL
        response = requests.get(url, timeout=10)

        # Parsing the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding all the forms present on the page
        forms = soup.find_all('form')

        # Displaying the number of forms found on the page
        print(colored(f"[+] Number of forms found on the page: {len(forms)}\n", 'blue'))

        # Loop through each form and print its details
        for i, form in enumerate(forms):
            print(colored(f"--- Form #{i + 1} ---", 'green'))

            # Get the action (URL to submit the form) and method (POST or GET)
            action = form.get('action')
            method = form.get('method', 'GET').upper()
            print(f"Action: {colored(action, 'yellow')}")
            print(f"Method: {colored(method, 'yellow')}")

            # Find all the input fields inside the form
            inputs = form.find_all('input')

            # Check if the form contains a password input (likely a login form)
            has_password = any(inp.get('type') == 'password' for inp in inputs)
            if has_password:
                print(colored("    [!] This might be a login form.", 'red'))

            # Print the details of each input field
            for inp in inputs:
                name = inp.get('name')
                type_ = inp.get('type')
                print(f"    [*] input - name: {colored(name, 'cyan')}, type: {colored(type_, 'cyan')}")
            print()

        # Asking the user if they want to scan another page
        user_input = input(colored("Do you want to scan another page? (y/n): ", 'yellow')).strip().lower()
        if user_input == 'y':
            new_url = input(colored("🔗 Enter the new URL to scan: ", 'yellow'))
            find_login_forms(new_url)  # Recursively call the function to scan a new URL
        else:
            print(colored("[+] Exiting... Stay secure!", 'blue'))

    except Exception as e:
        # Catch any errors that occur during the process
        print(colored(f"[!] Error loading the page: {e}", 'red'))


# Main entry point of the script
if __name__ == "__main__":
    url = input("🔗 Enter the URL to scan: ")  # Prompt the user to enter a URL
    find_login_forms(url)  # Start scanning the provided URL
