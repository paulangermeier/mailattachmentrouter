import re

prefix_list = ['WG:', 'Re:', 'Antw:', 'AW:', 'Antwort:', '[Extern]', '[External]', 'FW:', 'Fwd:']

subjects = [
    'Re: WG: 569: Wärmepumpen Angebot',
    'Angebot WG: Heizung ',
    '[External] 569 Angebot',
    'WG:',
    '',
    'RE: Straße 569',
    '   AW: 569 Angebot'
]

def remove_prefixes(subject, prefix_list):
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

assert remove_prefixes('Re: WG: 569: Wärmepumpen Angebot', prefix_list) == '569: Wärmepumpen Angebot', f'Ist: {remove_prefixes('Re: WG: 569: Wärmepumpen Angebot', prefix_list)!r}'
assert remove_prefixes('Angebot WG: Heizung ', prefix_list) == 'Angebot WG: Heizung ', f'Ist: {remove_prefixes('Angebot WG: Heizung ', prefix_list)!r}'
assert remove_prefixes('[Extern] 569 Angebot', prefix_list) == '569 Angebot', f'Ist: {remove_prefixes('[Extern] 569 Angebot', prefix_list)!r}'
assert remove_prefixes('WG:', prefix_list) == '', f'Ist: {remove_prefixes('WG:', prefix_list)!r}'
assert remove_prefixes('', prefix_list) == '', f'Ist: {remove_prefixes('', prefix_list)!r}'
assert remove_prefixes('RE: Straße 569', prefix_list) == 'Straße 569', f'Ist: {remove_prefixes('RE: Straße 569', prefix_list)!r}'
assert remove_prefixes('   AW: 569 Angebot', prefix_list) == '569 Angebot', f'Ist: {remove_prefixes('   AW: 569 Angebot', prefix_list)!r}'

adjusted_subjects = []

for subject in subjects:
    adjusted_subjects.append(remove_prefixes(subject, prefix_list))

for a in adjusted_subjects:
    print(a)

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

project_number_cases = [
    ('512 Angebot Lüftung', ('512', None)), #1
    ('1000 Neubau Schule', ('1000', None)), #2
    ('Urlaubsantrag', (None, None)), #3
    ('5a1 Test', ('5', None)), #4
    ('560-21 Angebot', ('560', '21')), #5
    ('560 Angebot', ('560', None)), #6
    ('', (None, None)), #7
    ('512Angebot', ('512', None)), #8
    ('560-', ('560', None)), #9
    ('560-Angebot', ('560', None)), #10
    ('560-20a', ('560', '20')), #11
    ('560-05 Angebot', ('560', '05')), #12
    ('560 -20', ('560', None)), #13 strikte Auslegung von R3; Sollwertänderung bei toleranter Schreibweise
    ('560- 20', ('560', None)), #14 strikte Auslegung von R3; Sollwertänderung bei toleranter Schreibweise
    ('560-21-3 Angebot', ('560', '21')), #15 Annahme: Es existieren keine Unter-Unterprojekte
    ('Angebot 512', (None, None)), #16 
    ('512 - 3 Angebote anbei', ('512', None)) #17
]

for eingabe, sollwert in project_number_cases:
    istwert = extract_project_numbers(eingabe)
    assert istwert == sollwert, f'Eingabe: {eingabe!r} \n Ist: {istwert!r} \n Soll: {sollwert!r}'

PROJECT_NUMBER_THRESHOLD = 500 # später nach config.py umziehen damit die Schwelle an einer zentralen Stelle ist

project_numbers = extract_project_numbers('Urlaubsantrag')

project_number_threshold_cases = [
    ('501', True),
    ('500', True),
    ('1000', True),
    ('499', False),
    ('104', False)
]

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

for eingabe, sollwert in project_number_threshold_cases: 
    istwert = check_project_number_threshold(int(eingabe), PROJECT_NUMBER_THRESHOLD)
    assert istwert == sollwert, f'Eingabe: {eingabe!r} \n Ist: {istwert!r} \n Soll: {sollwert!r}'
