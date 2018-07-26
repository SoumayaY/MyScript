import json
import csv
from LinkedinController import LinkedinController

linkedinTool = LinkedinController()
#urls = ['https://fr.linkedin.com/in/laurent-tabourot-99473318', 'https://fr.linkedin.com/in/christine-galez-30378248', 'https://fr.linkedin.com/in/laurence-vignollet-a353617']
urls=['https://www.linkedin.com/in/laurence-vignollet-a353617/']
for url in urls:
    profile = linkedinTool.extractProfile(url)
    x=json.dumps(profile, sort_keys=True, indent=4, ensure_ascii=False)
    x=json.loads(x)
    #print (x)
    f=csv.writer(open("result.csv","wt"))
    f.writerow(['NAME','NAME','NAME'])
    for x in x:
        f.writerow(x['NAME'],
                   x['SKILLS']['NAME'],
                   x['SKILLS']['NAME'])
    #print (json.dumps(profile, sort_keys=True, indent=4, ensure_ascii=False))

