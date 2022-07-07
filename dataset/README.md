## Dataset Field Description
#### Data Dictionary


| Data Label | DataType | Data Description | Examples |
|:----------:|:---:|:-------:|:---:|
| C/A | TEXT | Control Area name/Booth name. This is the internal identification of a booth at a given station. | **A002** (4 to 5 characters.) |
| UNIT | TEXT | Remote unit ID of station. | **R001**  (4 characters. A numeric designation preceded by ‘R’) |
| SCP | TEXT | Subunit/Channel/position represents a specific address for a given device. | **01-00-01** (Normally six characters in groups of 2 separated by a dash.) |
| STATION | TEXT | Station ID is the internal identification of a station. | **S002** (4 to 5 characters.) |
| LINENAME | TEXT | Represents all train lines that can be boarded at this station Normally lines are represented by one character. LINENAME 456NQR repersents train server for 4, 5, 6, N, Q, and R trains. | **456** (Variable data from 1 to 20 characters.) |
| DIVISION | TEXT | Represents the Line originally the station belonged to BMT, IRT, or IND. | **BMT** (3 character in length.) |
| DATE | DATE | Represents the date (MM-DD-YY). | **11/18/2014** |
| TIME | TIME | Represents the time (hhmmss) for a scheduled audit event. | **02:00:00** | 
| DESC | TEXT | Represent the REGULAR scheduled audit event (Normally occurs every 4 hours) 1. Audits may occur more that 4 hours due to planning, or troubleshooting activities. 2. Additionally, there may be a RECOVR AUD entry This refers to a missed audit that was recovered. | **REGULAR** |
| ENTRIES | NUMERIC | The comulative entry register value for a device. | **0001649720** |
| EXIST | NUMERIC | The cumulative exit register value for a device. | **0004863606** |