# Documentation
## 1. Create the Exel Table
### 1.1 Header Row Structure
In the first row of the Excel table, include the following column headers:

* `Topic`
* `Name`
* `Answer`
* `Description`
* `Active`
* `Title`
* `Payload`
* `Conditions`
* `Required_variables`
* `Start_actions`
* `End_actions`
* `Samples`
* `Intent`
## 1.2. Data Entry and Separation Methods
### Active:
  This column accepts the following values:
  
  `true` or `false`
  
  Alternatively, numeric representation: `1 (which represents true)`
### Title, Payload, Conditions, Required_variables, Start_actions, End_actions:
  Use the semicolon `;` as the delimiter to separate multiple values.
####  Example:
  ```
  Button1;Button2;Button3
  ```
  This means that multiple values (Button1, Button2, Button3) are separated by a semicolon.
### Samples, Intent:
  Use the vertical bar `|` as the delimiter to separate multiple values.
  
#### Example:
  ```
  Question1|Question2
  ```
Here, different variants such as questions or intents are separated by the `|` character.
## 2. Using Bot_Generator
### Launching the Generator Script
The provided script `Start_Generator.sh` is used to generate the bot based on the Excel data.
##### Parameters:
  * ##### dialogs.xlsx
    This is the path to the Excel file that contains the data structured as described above.
  * ##### output_directory
    This is the path to the directory where the output from the generator will be saved.
##### Example Command:
```
python3 Start_Generator.sh dialogs.xlsx output_directory
```
