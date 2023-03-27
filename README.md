# Introduction
This repo handles koders' attendance system from arduino's perspective

# Usage for attendance writer inside the card
- Burn Arduino/card_writer.ino file in arduino for writing using RC522 card writer and connect PINS according to the source code
- Run Serial Monitor and write employee id from official redmine url

# Usage for attendance reader
- Burn Arduino/card_reader.ino file in arduino for reading using RC522 card reader and connect PINS according to the source code
- Fill wifi ssid and password in the source code 
- Send the data to the server using http post request

# Contribution
For any contribution, please create a pull request
