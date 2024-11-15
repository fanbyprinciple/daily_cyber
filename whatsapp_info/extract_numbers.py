import re

def extract_phone_numbers(file_path):
 
  phone_numbers = []
  with open(file_path, 'r') as file:
    for line in file:
      # Use regular expression to find phone numbers in the line
      matches = re.findall(r'\+?\d[\d -]{8,12}\d', line) 
      for match in matches:
        phone_numbers.append(match)
  return phone_numbers

# Replace 'group_info.txt' with the actual file path
phone_numbers = extract_phone_numbers('group_info.txt')

if phone_numbers:
  print("Phone numbers found:")
  for number in phone_numbers:
    print(number)
else:
  print("No phone numbers found in the file.")