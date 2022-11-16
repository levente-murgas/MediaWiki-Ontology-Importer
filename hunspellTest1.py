from hunspell import Hunspell
import os

h = Hunspell('hu_HU',system_encoding='UTF-8')

stem = h.stem('anyád')
print(stem)