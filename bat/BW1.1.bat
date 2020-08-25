D:

call activate NCU

cd D:\python\crawler_NCU\BussnessWeekly

for /l %%c in (0, 1, 5) do (
   python BW_Main1.1.py %%c
)
pause