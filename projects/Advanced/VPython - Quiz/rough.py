import time

import datetime
import random
from psycopg2 import Timestamp

from pytz import HOUR
import tkinter as tk

# print(font.families())

# print(str(today)[:19])
# day_int = today.weekday()  # Monday starts at 0
# week_days = {idx: day for idx, day in enumerate(
#     ["Monday", "Tuesday", "Wednsday", "Thursday", "Friday", "Saturday", "Sunday"])}
# # print(week_days[day_int])

# data = [2, 4, 3, 5, 7, 8, 4, 1]
# print(random.choices(range(100), k=7))

# start_time = datetime.datetime.now()
# while 1:
#     time.sleep(1)
#     current_time = datetime.datetime.now()
#     diff = current_time - start_time
#     print(str(diff))
# # print(time.strftime(diff, '%M : %s'))


# ('Terminal', 'System', 'Fixedsys', 'Modern', 'Script', 'Roman', 'Courier', 'MS Serif', 'MS Sans Serif', 'Small Fonts', 'TeamViewer15', 'BILLY ARGEL FONT', 'Bethan', 'Bethan Thin', 'Bolt', 'Broadway Sans One', 'Broadway Sans One Rough', 'Broadway Sans Two', 'Broadway Sans Two Rough', 'Broadway Script', 'Broadway Script Rough', 'Broadway Serif', 'Broadway Serif Rough', 'Capslock', 'Carolin- Light', 'Carolin- Outline', 'Carolin-', 'Carolin- Thin', 'Cleantha', 'Cleantha Light', 'Cleantha Light Outline', 'Cleantha Thin', 'Comye', 'Dawnton Edge', 'Dawnton Ink', 'Dawnton Regular', 'Dawnton Rough', 'Dawnton Stamp', 'Duffish', 'Evina Light', 'Evina', 'Evina Thin', 'FIGHT BEAR', 'Fonseca Black Oblique', 'Fonseca Black', 'Fonseca Bold Oblique', 'Fonseca Bold', 'Fonseca ExtraBlack Oblique',
# 'Fonseca ExtraBlack', 'Fonseca ExtraBold Oblique', 'Fonseca ExtraBold', 'Fonseca Light Oblique', 'Fonseca Light', 'Fonseca Medium Oblique', 'Fonseca Medium',
# 'Fonseca Regular Oblique', 'Fonseca', 'Fonseca Thin Oblique', 'Fonseca Thin', 'Foundry Font Pack', 'Fresh Meat Four', 'Fresh Meat One', 'Fresh Meat Three', 'Fresh Meat Two', 'Hadeed', 'Immani Light', 'Immani', 'Ireene', 'Ireene Outline', 'Jadrien Light', 'Jadrien', 'Kadisoka Hand', 'Kadisoka Monoline', 'Kadisoka Sans', 'Kadisoka Script', 'Kadisoka Swash', 'Mahlon Light', 'Mahlon', 'Mahlon Thin', 'Newtype', 'Ocean Twelve Catchwords', 'Ocean Twelve Script', 'Ocean Twelve', 'Orion Black', 'Orion', 'Orion ExtraBold', 'Orion ExtraBold Italic', 'Orion Light', 'Orion SemiBold', 'Perkin Outline', 'Perkin', 'Seafool', 'TAGLINER', 'TAGLINER Swash', 'Thirdlone Ink', 'Thirdlone Regular', 'Thirdlone Stamp', 'Toxine', 'Xylon', 'Zenith', 'Zenith splatters', 'Affiliates', 'Belion', 'Bethan Light', 'ChatoBand', 'Giddyup Std', 'Marlett', 'SimSun-ExtB', '@SimSun-ExtB', 'KodchiangUPC', 'Kokila', 'Shonar Bangla', 'Mangal', 'BrowalliaUPC', 'Sakkal Majalla', 'LilyUPC', 'Palatino Linotype', 'MoolBoran', 'Franklin Gothic Medium', 'Cordia New', 'Arial', 'Arabic Transparent', 'Arial CE', 'Arial Greek', 'Arial Baltic', 'Arial TUR', 'Arial CYR', 'AngsanaUPC', 'JasmineUPC', 'Trebuchet MS', 'Microsoft Tai Le', 'Utsaah', 'Malgun Gothic', '@Malgun Gothic', 'Simplified Arabic Fixed', 'Gisha', 'Microsoft JhengHei Light', '@Microsoft JhengHei Light', 'Microsoft JhengHei UI Light', '@Microsoft JhengHei UI Light', 'Comic Sans MS', 'Segoe UI Symbol', 'Vrinda', 'FreesiaUPC', 'Traditional Arabic', 'Aparajita', 'Sitka Small', 'Sitka Text', 'Sitka Subheading', 'Sitka Heading', 'Sitka Display', 'Sitka Banner', 'Nirmala UI Semilight', 'Leelawadee UI', 'Gadugi', 'Microsoft New Tai Lue', 'DokChampa', 'Segoe UI', 'Calibri', 'Miriam', 'Angsana New', 'Iskoola Pota', 'Kartika', 'Segoe UI Semilight', 'Vijaya', 'Nirmala UI', 'Mongolian Baiti', 'Microsoft YaHei', '@Microsoft YaHei', 'Microsoft YaHei UI', '@Microsoft
# YaHei UI', 'Vani', 'Arial Black', 'IrisUPC', 'Batang', '@Batang', 'BatangChe', '@BatangChe', 'Gungsuh', '@Gungsuh', 'GungsuhChe', '@GungsuhChe', 'Gautami', 'Segoe UI Black', 'Calibri Light', 'Cambria', 'Rod', 'Georgia', 'Verdana', 'Symbol', 'Euphemia', 'Raavi', 'Corbel', 'Shruti', 'Consolas', 'Segoe UI Semibold', 'Simplified Arabic', 'Cambria Math', 'DaunPenh', 'Nyala', 'Constantia', 'Yu Gothic', '@Yu Gothic', 'CordiaUPC', 'Khmer UI', 'Aharoni', 'Microsoft Uighur', 'Times New Roman', 'Times New Roman CYR', 'Times New Roman TUR', 'Times New Roman CE', 'Times New Roman Baltic', 'Times New Roman Greek', 'Segoe Script', 'Candara', 'Ebrima', 'DilleniaUPC', 'MS Mincho', '@MS Mincho', 'MS PMincho', '@MS PMincho', 'Browallia New', 'Segoe UI Light', 'Segoe UI Emoji', 'Aldhabi', 'DFKai-SB', '@DFKai-SB', 'SimHei', '@SimHei', 'Lao UI', 'Courier New', 'Courier New CYR', 'Courier New TUR', 'Courier New CE', 'Courier New Greek', 'Courier New Baltic', 'Kalinga', 'Microsoft PhagsPa', 'Tahoma', 'EucrosiaUPC', 'KaiTi', '@KaiTi', 'SimSun', '@SimSun', 'NSimSun', '@NSimSun', 'Meiryo', '@Meiryo', 'Meiryo UI', '@Meiryo UI', 'Sylfaen', 'Tunga', 'Urdu Typesetting', 'Microsoft YaHei Light', '@Microsoft YaHei Light', 'Microsoft YaHei UI Light', '@Microsoft YaHei UI Light', 'Webdings', 'Plantagenet Cherokee', 'Gabriola', 'MS Gothic', '@MS Gothic', 'MS UI Gothic', '@MS UI Gothic', 'MS PGothic', '@MS PGothic', 'Gulim', '@Gulim',
# 'GulimChe', '@GulimChe', 'Dotum', '@Dotum', 'DotumChe', '@DotumChe', 'Lucida Sans Unicode', 'Andalus', 'Leelawadee', 'FangSong', '@FangSong', 'Yu Mincho Demibold', '@Yu Mincho Demibold', 'David', 'Miriam Fixed', 'Impact', 'Levenim MT', 'Segoe Print', 'Estrangelo Edessa', 'Leelawadee UI Semilight', 'Microsoft JhengHei', '@Microsoft JhengHei', 'Microsoft JhengHei UI', '@Microsoft JhengHei UI', 'Narkisim', 'MingLiU-ExtB', '@MingLiU-ExtB', 'PMingLiU-ExtB', '@PMingLiU-ExtB', 'MingLiU_HKSCS-ExtB', '@MingLiU_HKSCS-ExtB', 'Yu Mincho Light', '@Yu Mincho Light', 'Latha', 'Microsoft Sans Serif', 'FrankRuehl', 'MingLiU', '@MingLiU', 'PMingLiU', '@PMingLiU', 'MingLiU_HKSCS', '@MingLiU_HKSCS', 'Myanmar Text', 'Yu Gothic Light', '@Yu Gothic Light', 'Javanese Text', 'Microsoft Himalaya', 'Yu Mincho', '@Yu Mincho', 'Lucida Console', 'Arabic Typesetting', 'Microsoft Yi Baiti', 'MV Boli', 'Wingdings', 'Century', 'Wingdings 2', 'Wingdings 3', 'Arial Narrow', 'Book Antiqua', 'Garamond', 'Monotype Corsiva', 'Bookman Old Style', 'Tempus Sans ITC', 'Mistral', 'Lucida Handwriting', 'Kristen ITC', 'Juice ITC', 'Freestyle Script', 'Century Gothic', 'Algerian', 'Baskerville Old Face', 'Bauhaus 93', 'Bell MT', 'Berlin Sans FB', 'Bernard MT Condensed', 'Bodoni MT Poster Compressed', 'Britannic Bold', 'Broadway', 'Brush Script MT', 'Californian FB', 'Centaur', 'Chiller', 'Colonna MT', 'Cooper Black', 'Footlight MT Light', 'Harlow Solid Italic', 'Harrington', 'High Tower Text', 'Jokerman', 'Kunstler Script', 'Lucida Bright', 'Lucida Calligraphy', 'Lucida Fax', 'Magneto', 'Matura MT Script Capitals', 'Modern No. 20', 'Niagara Engraved', 'Niagara Solid', 'Old English Text MT', 'Onyx', 'Parchment', 'Playbill', 'Poor Richard', 'Ravie', 'Informal Roman', 'Showcard Gothic', 'Snap ITC', 'Stencil', 'Viner Hand ITC', 'Vivaldi', 'Vladimir Script', 'Wide Latin', 'Berlin Sans FB Demi', 'MT Extra', 'Pristina', 'Papyrus', 'French Script MT', 'Bradley Hand ITC', 'MS Outlook', 'Bookshelf Symbol 7', 'MS Reference Sans Serif', 'MS Reference Specialty', 'Droid Sans Mono Slashed', 'Arvo', 'Droid Serif', 'Indie Flower', 'Lobster', 'Open Sans', 'Poiret One', 'Raleway', 'Roboto', 'Roboto Condensed', 'Roboto Slab', 'Lato Black', 'Lato', 'Lato Hairline', 'Lato Light', 'A Charming Font Expanded', 'A Charming Font', 'Adine Kirnberg', 'Blackletter', 'Forsaken Outline', 'Forsaken', 'Haste', 'Ringstown Alternate', 'Ringstown Dry', 'Ringstown', 'Adine Kirnberg Alternate', 'Blackwood Castle', 'Chang and Eng', 'Chopin Script', 'Clerica', 'Coca Cola ii', 'Coelnische Current Fraktur OsF', 'Coelnische Current Fraktur', 'Colchester', 'Corazon', 'Cretino', 'Curlz MT', 'Delta Hey Max Nine', 'Dobkin Script',
# 'Dope Jam', 'Dumbledor 3 Cut Up', 'EmbossedBlack', 'EmbossedBlackWide', 'EmporiumCapitals', 'EVOL', 'Extraction BRK', 'fack', 'Fancy Card Text', 'Felix Titling', 'Festival', 'Freebooter Script', 'Gabrielle', 'Gebetbuch Fraktur', 'Germania Versalien', 'Gingerbread Initials', 'Ginko', 'Gotham Thin', 'Grusskarten Gotisch', 'Guevara', 'HEATWAVE', 'Heavy Texture', 'Highway to Heck', 'Heidorn Hill', 'HenryMorganHand', 'hypografic', 'Iglesia', 'It Lives In The Swamp BRK', 'Blackadder ITC', 'Edwardian Script ITC', 'JaggaPoint', 'Jolt Of Caffeine BRK', 'Kanzlei')
# available_recs_count = [(1,12),(2,3)]
# available_recs = [some for some[0] in available_recs_count]
# print(available_recs)
# # print(0==False)
# import os 
# from configparser import ConfigParser

# list_ = [1,2,3,4,5,6,7,8,9]
# tuple_= ('a','b','c','d')
# str_ = 'abdhss'

# # for item in zip(list_,str_):
# #     print(item)
# # # Result
# # # (1, 'a')
# # (2, 'b')
# # (3, 'd')
# # (4, 'h')
# # (5, 's')
# # (6, 's')

# list_.remove()
# print(list_)

from playsound import playsound
import threading

# playsound("Sound_effects\ding_s.mp3")
threading.Thread(target=playsound,args = ["Sound_effects\ding_s.mp3"],name = 'self.music_thread').start()
print(dir(threading.Thread))
print(threading.Thread.join)
print(threading.Thread.is_alive)