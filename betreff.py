import re

PREFIX_LIST = ['WG:', 'Re:', 'Antw:', 'AW:', 'Antwort:', '[Extern]', '[External]', 'FW:', 'Fwd:']

def remove_prefixes(subject, prefix_list):
    """Entfernt bekannte Präfixe am Betreffanfang (R1).

    Erwartet den Betreff (subject) als String und eine Liste mit Präfix-Strings (prefix_list).
    
    Eine Schleife entfernt so lange Präfixe, bis keines mehr vorne steht (WG:, AW:, RE: ...)
    dabei ist Groß- und Kleinschreibung nicht relevant.
    Führende Leerzeichen und Leerzeichen nach dem Präfix werden entfernt.
    Präfixe mitten im Betreff werden nicht entfernt, darum kümmert sich R2.

    Zurückgegeben wird der bereinigte Betreff als String:
        "WG: AW: 512 Rückfrage"     -> "512 Rückfrage"
        "Angebot AW: 512"           -> "Angebot AW: 512"
        "AW: WG: RE:"               -> ""
        "aw: 512: Angebot"          -> "512: Angebot"
    """
    adjusted_subject = subject.lstrip()
    flag = True

    while flag:
        flag = False
        for prefix in prefix_list:
            if adjusted_subject.upper().startswith(prefix.upper()):
                # Annahme: in den Präfixen kommen keine Zeichen vor 
                # die durch .upper() ihre Länge ändern
                adjusted_subject = adjusted_subject[len(prefix):] 
                adjusted_subject = adjusted_subject.lstrip()
                flag = True

    return adjusted_subject

def extract_project_numbers(subject):
    """Liest Haupt- und Unternummer am Anfang des Betreff aus (R2, R3).

    Erwartet den Betreff nach R1 (Präfixe bereits entfernt).
    Gibt ein Tupel (Hauptnummer, Unternummer) zurück: 
        '512 Angebot'       -> ('512', None)
        '560-21 Angebot'    -> ('560', '21')
        'Urlaubsantrag'     -> (None, None)

    Rückgabe als Strings, nicht als int: führende Nullen bleiben erhalten,
    und R5/R6 vergleichen ohnehin mit Ordnernamen. Umwandlung in int erst in R4.

    R3 strikt: Unternummer nur bei Bindestrich ohne Leerzeichen ('560-20').
    '560 - 20' ergibt bewusst ('560', None), tolerante Schreibweise ist eine offene
    Frage in der Spezifikation.
    """
    # re.match, weil die Nummer laut R2 und Firmen-Konvention am 
    # Anfang des Betreffs stehen muss
    match = re.match(r'(\d+)(?:-(\d+))?', subject)
    if match is None: 
        return (None, None)
    return match.groups()

def check_project_number_threshold(project_number, project_number_threshold):
    """Prüft ob die Projektnummer gleich oder über der vorgegebenen Schwelle liegt (R4). 

    Erwartet die Hauptnummer als int (project_number), das aus dem Tupel von 
    extract_project_numbers im Aufruf erzeugt wird und die Schwelle als int 
    (project_number_threshold).
    None als Eingabe wird nicht abgefangen; Bevor die function aufgerufen wird, muss 
    geprüft werden ob extract_project_numbers überhaupt eine Hauptnummer geliefert hat.

    Gibt ein Bool bei Schwelle 500 zurück: 
        500     -> True
        1000    -> True
        499     -> False

    True bedeutet, die Mail wird weiter verarbeitet.
    False bedeutet, die Mail wird ignoriert.
    """
    if project_number < project_number_threshold:
        return False
    return True


