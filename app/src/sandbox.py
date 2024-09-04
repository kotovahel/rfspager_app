import time
import datetime
import json


sl = {'2024-09-04 20:54 0134011': 'FRINC TYPE: MVA TURNOUT: AP340 INC: 157378-04092024', '2024-09-04 18:24 0107811': 'FRINC TYPE: MVA PERSONS TRAPPED TURNOUT: RP78 INC: 157290-04092024', '2024-09-04 18:23 0109011': 'FRINC TYPE: MVA TURNOUT: CT90 INC: 157287-04092024', '2024-09-04 18:22 0109011': 'FRINC TYPE: MVA TURNOUT: P90 INC: 157287-04092024', '2024-09-04 17:51 0108811': 'FRINC TYPE: MVA TURNOUT: CT88 INC: 157246-04092024', '2024-09-04 17:38 0108811': 'FRINC TYPE: MVA TURNOUT: CP88 INC: 157246-04092024', '2024-09-04 17:28 0107811': 'FRINC TYPE: MVA PERSONS TRAPPED TURNOUT: RP78 INC: 157236-04092024', '2024-09-04 16:43 0135711': 'FRINC TYPE: MVA PERSONS TRAPPED TURNOUT: RP357,TR357 INC: 157205-04092024'}
print(len(sl))
sorted_sl = dict(sorted(sl.items()))
print(sorted_sl)


previous_messages = {x: y for x, y in list(sorted_sl.items())[4:]}
print(previous_messages)


