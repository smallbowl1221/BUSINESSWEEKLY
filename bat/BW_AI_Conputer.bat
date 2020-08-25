call activate LCH

cd 

for /l %%c in (0, 1, 5) do (
   python BW_Main.py %%c
)
pause