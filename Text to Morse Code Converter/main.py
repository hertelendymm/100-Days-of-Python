morse_code_abc = {
  'a': '·−',
  'b': '−···',
  'c': '−·−·',
  'd': '−··',
  'e': '·',
  'f': '··−·',
  'g': '−−·',
  'h': '····',
  'i': '··',
  'j': '·−−−',
  'k': '−·−',
  'l': '·−··',
  'm': '−−',
  'n': '−·',
  'o': '−−−',
  'p': '·−−·',
  'q': '−−·−',
  'r': '·−·',
  's': '···',
  't': '−',
  'u': '··−',
  'v': '···−',
  'w': '·−−',
  'x': '−··−',
  'y': '−·−−',
  'z': '−−··',
  '0': '−−−−−',
  '1': '·−−−−',
  '2': '··−−−',
  '3': '···−−',
  '4': '····−',
  '5': '·····',
  '6': '−····',
  '7': '−−···',
  '8': '−−−··',
  '9': '−−−−·',
  ' ': '/'
}

# Welcome ascii app logo
print('''
 _____         _     _         ___  ___                      _____           _        _____                           _            
|_   _|       | |   | |        |  \/  |                     /  __ \         | |      /  __ \                         | |           
  | | _____  _| |_  | |_ ___   | .  . | ___  _ __ ___  ___  | /  \/ ___   __| | ___  | /  \/ ___  _ ____   _____ _ __| |_ ___ _ __ 
  | |/ _ \ \/ / __| | __/ _ \  | |\/| |/ _ \| '__/ __|/ _ \ | |    / _ \ / _` |/ _ \ | |    / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__|
  | |  __/>  <| |_  | || (_) | | |  | | (_) | |  \__ \  __/ | \__/\ (_) | (_| |  __/ | \__/\ (_) | | | \ V /  __/ |  | ||  __/ |   
  \_/\___/_/\_\\__|  \__\___/  \_|  |_/\___/|_|  |___/\___|  \____/\___/ \__,_|\___|  \____/\___/|_| |_|\_/ \___|_|   \__\___|_|
''')

# Asking user for a text input or escape command
text = str(input("\nType something you want to convert from text to Morse code (or \"exit\" when you're done):\n")).lower()
while text != "exit":
  # Convert the text input to morse code
  converted_char_list = [morse_code_abc[character] for character in text]
  morse_code = ' '.join(converted_char_list)
  print(f'The Morse Code of \"{text}\" is: {morse_code}')

  # Asking user for a text input or escape command
  text = str(input("\nType something you want to convert from text to Morse code (or \"exit\" when you're done):\n")).lower()
