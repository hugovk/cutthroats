# Finding cutthroats in OpenStreetMap

## What are cutthroat compounds?

* http://www.encyclopediabriannica.com/?p=57


## A selection of potential cutthroats discovered

* Blowhorn Street
* Crackbottle Road (also a [1608 Roger Crack-Bottle](https://archive.org/stream/ReportOnTheManuscriptsOfTheMarquessOfDownshireV2/Manuscripts_Marquess_of_Downshire_v2#page/n119/mode/2up/search/crack-bottle) and [1897 Major Crackbottle](http://chroniclingamerica.loc.gov/lccn/sn88053055/1897-09-30/ed-1/seq-3/#date1=1789&index=1&rows=20&words=Crackbottle&searchType=basic&sequence=0&state=&date2=1924&proxtext=crackbottle&y=0&x=0&dateFilterType=yearRange&page=1))
* Jinglepot Bridge
* Jingle Pot and Hurtle Pot caves
* Killcat Wood
* Rackstraw Road/Grove (also a surname, perhaps a farm contractor assisting the harvest [source](http://www.surnamedb.com/Surname/Rackstraw))
* Rattlebone Inn ("named after local hero John Rattlebone, killed in the Battle of Sherston in 1016." [source](http://www.dailymail.co.uk/news/article-94484/The-Rattlebone-Inn.html))
* Rattlechain Lagoon
* Saylittle Mews
* Shatterstone (also a place in Game of Thrones, a plateau in the shadow of an exploding volcano in World of Warcraft, a spell in Guid Wars, a mage ability in Dragon Age that explodes a boulder, a mine in Skyrim, and in many other fantasy things)
* Scratchface Lane (lots of 'em!) and Scratchface Copse
* Slaparse Lane (possibly from a red light district next to a garrison) (cf. Sainct Frappecul, St. Slaparse; Slap-Arse Swamp; farmer Slap-arse Wharton)
* Splitwind Pond/Island ("Owing to some physical peculiarity, the wind south of this island is often very different from that north of it." [source](https://data.aad.gov.au/aadc/gaz/display_name.cfm?gaz_id=132030))
* Squeezebelly Lane/Alley ("one of the narrowest public thoroughfares in the UK. The person in this shot is at about the narrowest part." [source](https://www.seriouscompacts.com/media/squeeze-belly-lane-from-the-bottom.4130/))
* Starvehouse Mine ("The ominous-sounding Starvehouse mine, on Cop Rake, had an earlier and more optimistic title – New York. Our confabulations about places often drift towards the negative, even the malign." [source](https://www.theguardian.com/environment/2013/dec/30/conies-dale-derbyshire-courting-ravens))
* Stealgoose Drain
* Stickletongue Beck through Stickletongue Wood
* Tickleback Row
* Ticklebelly Alley
* Ticklepenny Lock/Lane


## Summary of output files

* england-highways.csv - highways in England
  * england-highways-cutthroats.txt - 9,555 potential cutthroats beginning with a known cutthroat verb
  * england-highways-cutthroats2.txt - 329 potential cutthroats of a known cutthroat verb+noun

* england.csv - place names in England
  * england-cutthroats.txt - 14,580 potential cutthroats beginning with a known cutthroat verb
  * england-cutthroats2.txt - 489 potential cutthroats of a known cutthroat verb+noun

Search https://www.openstreetmap.org with the potential cutthroat to find full names and location containing it.


## How to find potential cutthroats in English street names

1. We'll use some Python scripts to search for cutthroats, so let's fetch that and do everything from the same directory.
```bash
git clone https://github.com/hugovk/cutthroats
cd cutthroats
```

2. Download [england-latest.osm.pbf](http://download.geofabrik.de/europe/great-britain/england-latest.osm.pbf) (718 MB) from http://download.geofabrik.de/europe/great-britain.html

3. We'll use [osmfilter](https://wiki.openstreetmap.org/wiki/Osmfilter) to filter for street names. To allow fast data processing, they recommend using .o5m format for input, so we'll use [osmconvert](https://wiki.openstreetmap.org/wiki/Osmconvert) for that, and also to convert it to a text file. Download or install osmconvert (eg. download a binary) and osmfilter (eg. `brew install osmfilter`).

4. Convert the pbf to o5m:
```bash
osmconvert england-latest.osm.pbf -o=england-latest.o5m
```
<sub>(28s, 718M -> 1.3G)</sub>

5. Filter and keep all the highways ([eg.](https://wiki.openstreetmap.org/wiki/Osmfilter#Object_Filter))
```bash
osmfilter england-latest.o5m --keep="highway=" -o=england-highways.o5m
```
<sub>(18s, 1.3G -> 412M)</sub>

6. Write that out to a text file using CSV format ([eg.](https://wiki.openstreetmap.org/wiki/Osmconvert#Writing_CSV_Files)), and remove duplicates
```bash
osmconvert england-highways.o5m --csv=name -o=england-highways.csv
```
<sub>(3s, 412M->21M, 1 478 885 lines)</sub>

7. Sort and remove duplicates
```bash
sort -u england-highways.csv > 2.csv && mv 2.csv england-highways.csv
```
<sub>(28s, 21M->6.2M, 390 368 lines)</sub>

8. Look for cutthroats

Given some known cutthroats, find their verb- stems. Then given the CSV of names, find other words beginning with those verbs.
They might be new cutthroats!

```bash
pip install -r requirements.txt
python cutthroat-finder.py -f england-highways.csv > england-highways-cutthroats.txt
```
<sub>(25s, 6.2M -> 89K, 9 724 lines, 9 555 potential new cutthroats)</sub>

The repeat but only return potential cutthroats that also end in known -nounstems.
Fewer results, but better chance of cutthroats?

```bash
python cutthroat-finder.py -f england-highways.csv --match-nouns > england-highways-cutthroats2.txt
```
<sub>(25s, 6.2M -> 4.3K, 468 lines, 329 potential new cutthroats)</sub>

## How to find potential cutthroats in English place names

Let's repeat but on all place names in England, not just the highways.
Basically steps 1-4 as above, skip the filtering in step 5, and steps 6-10 from england-latest.o5m.

6. Write that out to a text file using CSV format ([eg.](https://wiki.openstreetmap.org/wiki/Osmconvert#Writing_CSV_Files)), and remove duplicates
```bash
osmconvert england-latest.o5m --csv=name -o=england.csv
```
<sub>(10s, 1.3G->34M, 2 313 803 lines)</sub>

7. Sort and remove duplicates
```bash
sort -u england.csv > 2.csv && mv 2.csv england.csv
```
<sub>(48s, 34M->15M, 845 787 lines)</sub>

8. Look for cutthroats

Given some known cutthroats, find their verb- stems. Then given the CSV of names, find other words beginning with those verbs.
They might be new cutthroats!

```bash
pip install -r requirements.txt
python cutthroat-finder.py -f england.csv > england-cutthroats.txt
```
<sub>(53s, 15M -> 135K, 14 841 lines, 14 580 potential new cutthroats)</sub>

The repeat but only return potential cutthroats that also end in known -nounstems.
Fewer results, but better chance of cutthroats?

```bash
python cutthroat-finder.py -f england.csv --match-nouns > england-cutthroats2.txt
```
<sub>(52s, 15M -> 6.4K, 702 lines, 489 potential new cutthroats)</sub>
