KURSE = {
    # entsprechend der kursliste eintragen
}

schulnummer = 123

ACTUAL_KURSE = {}
for schüler in KURSE:
    KURS_DATEN = KURSE[schüler].split()
    for kurs in KURS_DATEN:
        if kurs not in ACTUAL_KURSE:
            ACTUAL_KURSE[kurs] = []
        
        ACTUAL_KURSE[kurs].append(schüler)

FACH_NAMEN = {
    "de": "Deutsch",
    "en": "Englisch",
    "spa": "Spanisch",
    "ku": "Kunst",
    "ge": "Geschichte",
    "grw": "G/R/W",
    "geo": "Geographie",
    "ma": "Mathematik",
    "ph": "Physik",
    "eth": "Ethik",
    "spol": "Sport (Leichtathletik)",
    "inf": "Informatik",
    "com": "Computermathematik",
    "fr": "Französisch",
    "bio": "Biologie",
    "ch": "Chemie",
    "spok": "Sport (Kampfsport)",
    "mu": "Musik",
    "ree": "Religion",
    "spog": "Sport (Geräteturnen)",
    "spa": "Spanisch",
    "mus": "Musik",
    "en": "Englisch",
    "---": "---"
}

remove_numbers = lambda x: ''.join([i for i in x if not i.isdigit()])

class Unterricht:
    def __init__(self, stunde, fach, lehrer, zimmer, bemerkungen):
        self.stunde = stunde
        self.fach = fach
        self.lehrer = lehrer
        self.zimmer = zimmer
        self.bemerkungen = bemerkungen

    def schüler_in_kurs(self, schüler):
        if self.fach == "---":
            if not self.bemerkungen:
                return True
            
            bemerkungen = self.bemerkungen.split()[0]
            if bemerkungen in ACTUAL_KURSE:
                if schüler in ACTUAL_KURSE[bemerkungen]:
                    return True
                return False
            
            return False
        
        if self.fach in ACTUAL_KURSE:
            if schüler in ACTUAL_KURSE[self.fach]:
                return True
            return False
        
    def to_dict(self):
        return {
            "stunde": self.stunde,
            "fach": self.fach,
            "lehrer": self.lehrer,
            "zimmer": self.zimmer,
            "bemerkungen": self.bemerkungen
        }

        
class Klausur:
    def __init__(self, jahrgang, kurs, kursleiter, stunde, beginn, dauer, info, raum):
        self.jahrgang = jahrgang
        self.kurs = kurs
        self.kursleiter = kursleiter
        self.stunde = stunde
        self.beginn = beginn
        self.dauer = dauer
        self.info = info
        self.raum = raum
        self.fach = FACH_NAMEN[remove_numbers(kurs.lower())]

    def get_schüler(self):
        return ACTUAL_KURSE[self.kurs]
    
    def __str__(self):
        return f"""
**Kurs**: {self.kurs} ({self.fach})
**Kursleiter**: {self.kursleiter}
**Beginn**: {self.beginn}
**Dauer**: {self.dauer}
**Info**: {self.info}
**Raum**: {self.raum}
**Schüler**:
```
{', '.join(self.get_schüler())}
```"""
    
    def to_dict(self):
        return {
            "jahrgang": self.jahrgang,
            "kurs": self.kurs,
            "kursleiter": self.kursleiter,
            "stunde": self.stunde,
            "beginn": self.beginn,
            "dauer": self.dauer,
            "info": self.info,
            "raum": self.raum
        }
