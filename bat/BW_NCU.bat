D:

call activate LCH

cd D:\python\crawler_NCU\BUSINESSWEEKLY

for /l %%c in (0, 1, 5) do (
   python BW_Main.py %%c
)
pause