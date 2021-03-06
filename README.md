# PTCPasswordChanger
Use webdriver to change ptc account password automatically.

# Installation
To install PTC-AutoChange-Password run:
```
git clone git@github.com:weizh888/PTC-AutoChange-Password.git
```
Then:
```
cd PTC-AutoChange-Password
```

# Usage
To use the program run the following command:
```
python change_password.py -f accounts.csv -pw password
```
Where **accounts.csv** is the file of accounts to change password, and **password** is the new password. See "Formatting" to see how they should be formatted.

# Formatting
* The **accounts** file supports two types of structures as follows:
  - RocketMap Format
  ```ptc,PTCAccount001,Example001!```
  - Another Format
  ```PTCAccount002:Example002!```
* The **new password** should follow the rules:
  > Your password must include at least one uppercase and one lowercase letter, a number, and at least one other character that is not a letter or digit, such as *, ', (, etc.
  
# Output
The program will display a message in the terminal if the password is changed. Additionally, it will output all password-changed accounts to a new file named **succeed.csv**, and all accounts that failed to change password to **failed.csv**.
