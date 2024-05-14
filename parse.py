import requests
import datetime
import xmltodict
import discord

from constants import FACH_NAMEN, remove_numbers, Klausur, Unterricht, schulnummer

class Parser:
    def __init__(self, in_days, klasse="11"):

        day = datetime.datetime.now() + datetime.timedelta(days=in_days)
        self.weekday = day.weekday()
        self.get_authorization(in_days)

        # die cookies interessieren einen nicht, da die API die gesamten daten ausspuckt
        self.cookies = {
            "Planart": "0",
            "Klasse": "11",
        }

        self.headers = {
            "authorization": "Basic Base64Encoded(Username:Password)"
        }

        self.klasse = klasse

        r = requests.get(self.url, cookies=self.cookies, headers=self.headers)
        self.xml = xmltodict.parse(r.text) if r.text else None

    # extreme pro gamer authorization
    def get_authorization(self, in_days):
        day = datetime.datetime.now() + datetime.timedelta(days=in_days)
        now = datetime.datetime.now().timestamp()
        authtimestamp = str(now).split(".")[0]+str(now).split(".")[1][:3]
        authday = f"{day.year}{'0'+str(day.month) if day.month < 10 else day.month}{'0'+str(day.day) if day.day < 10 else day.day}"
        self.url = f"https://www.stundenplan24.de/{schulnummer}/wplan/wdatenk/WPlanKl_{authday}.xml?_="+authtimestamp
        
    def weekday_to_string(self):
        weekdays = {
            0: "Montag",
            1: "Dienstag",
            2: "Mittwoch",
            3: "Donnerstag",
            4: "Freitag",
            5: "Samstag",
            6: "Sonntag",
        }
        return weekdays.get(self.weekday, "Unbekannt")

    def renew(self, in_days):
        self.get_authorization(in_days)
        r = requests.get(self.url, cookies=self.cookies, headers=self.headers)
        self.xml = xmltodict.parse(r.text) if r.text else None

    def get_data(self):
        if not self.xml:
            return

        classes = self.xml.get("WplanVp", {}).get("Klassen", {}).get("Kl", [])
        for c in classes:
            if c.get("Kurz") == self.klasse:
                fächer = c.get("Pl", {}).get("Std", [])
                for f in fächer:
                    fach_kuerzel = f.get("Fa") if type(f.get("Fa")) is not dict else f.get("Fa", {}).get("#text")
                    unterricht = Unterricht(
                        f.get("St"),
                        fach_kuerzel,
                        f.get("Le") if type(f.get("Le")) is not dict else f.get("Le", {}).get("#text") if str(f.get("Le", {}).get("#text")) != "&nbsp;" else "---",
                        f.get("Ra") if type(f.get("Ra")) is not dict else f.get("Ra", {}).get("#text") if str(f.get("Ra", {}).get("#text")) != "&nbsp;" else "---",
                        f.get("If")
                    )
                    yield unterricht

    def get_klausuren(self):
        if not self.xml:
            return

        classes = self.xml.get("WplanVp", {}).get("Klassen", {}).get("Kl", [])
        for c in classes:
            if c.get("Kurz") == self.klasse:
                klausuren = c.get("Klausuren", {}).get("Klausur", [])
                if type(klausuren) is not list:
                    klausuren = [klausuren]
                for k in klausuren:
                    klausur = Klausur(
                        k.get("KlJahrgang"),
                        k.get("KlKurs"),
                        k.get("KlKursleiter"),
                        k.get("KlStunde"),
                        k.get("KlBeginn"),
                        k.get("KlDauer") + " Minuten",
                        k.get("KlKinfo"),
                        k.get("KlRaum", "Aula")
                    )
                    yield klausur

    def make_embed(self, schueler):
        if not self.xml:
            embed = discord.Embed(
                title="Fehler",
                description="Der Stundenplan konnte nicht geladen werden.",
                color=discord.Color.red()
            )
            return embed
        
        embed = discord.Embed(
            title=f"Stundenplan für {schueler}",
            description=f"Stundenplan für den {self.weekday_to_string()}",
            color=discord.Color.green()
        )

        for item in self.get_data():
            if item.schüler_in_kurs(schueler):
                embed.add_field(
                    name=f"{item.stunde}. Stunde",
                    value=f"**Fach:** {FACH_NAMEN[remove_numbers(item.fach.lower())]}\n**Lehrer:** {item.lehrer}\n**Raum:** {item.zimmer}\n**Bemerkungen:** {item.bemerkungen}",
                    inline=False
                )

        return embed


