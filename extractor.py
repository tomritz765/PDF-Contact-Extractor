import PyPDF2
import re
import os
import csv

#1.Setup: Define pattern for Email and Phone 
# This is "Regex" -the secret to professional data extraction
EMAIL_REGEXP = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_REGEXP = r'\b\d{10}\b' #10 digits Mobile Number

def extract_data_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb')as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text +=page.extract_text()

            emails = re.findall(EMAIL_REGEXP,text)
            phones = re.findall(PHONE_REGEXP,text)

            return emails, phones
    except Exception as e:
        print(f"Error reading {file_path}:{e}")
        return [], []

def main():
    #Path where your PDFs are store (Current folder)
    folder_path = './'
    result = []

    print("-----Starting Extraction-----")

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            print(f"Processing:{file}")
            emails,phones = extract_data_from_pdf(file) 

            #Save result with filename
            result.append({
                'File':file,
                'Emails':",".join(emails),
                'Phones': ",".join(phones)
            })                

    # 2. Export to CSV 
    if result:
        keys = result[0].keys()
        with open('extracted_contacts.csv','w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(result)

        print(f"\nSuccess! Data saved to 'extracted_contacts.csv'")
    else:
        print("\nNo data extracted to save.")

if __name__=="__main__":
    main()
#__________-----------------------__________________