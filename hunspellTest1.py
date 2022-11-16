from hunspell import Hunspell

h = Hunspell('hu_HU', hunspell_data_dir=r'C:\Users\murga\OneDrive\Documents\GitHub\temalab\dicts')

h2 = Hunspell()
stem = h2.stem('savers')
print(stem)