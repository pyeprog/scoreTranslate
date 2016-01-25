#Simple score to midi score
The lastest version is music\_v3.py

#Usage
python music\_v3.py [A-G] [scale] ["simple score" | filename]

#Format of simple score
- Use space to divide note
- Note should be between 1 - 7
- Several u or d can be append to note to specify key up or down, e.g. 2u 4uu 3uuu 1d 4dd 1ddd
- '|' can be used to divide different segment
- Feel free to start a new line
- Lines of same number of segments will be filled in same table

#Feature
- Extra space is tolerated 
- Argument 3 can be string of simple score or the name of a score file with the right format
