from betreff import remove_prefixes, extract_project_numbers, check_project_number_threshold

TEST_PREFIX_LIST = ['WG:', 'Re:', 'Antw:', 'AW:', 'Antwort:', '[Extern]', '[External]', 'FW:', 'Fwd:']
TEST_PROJECT_NUMBER_THRESHOLD = 500 # Bei Veränderung der Schwelle sind die project_number_threshold_cases anzupassen

# Test um das Entfernen der Präfixe durch remove_prefixes zu prüfen

subject_cases = [
    ('Re: WG: 569: Wärmepumpen Angebot', '569: Wärmepumpen Angebot'),
    ('Angebot WG: Heizung ',  'Angebot WG: Heizung '),
    ('[External] 569 Angebot', '569 Angebot'),
    ('WG:', ''),
    ('', ''),
    ('RE: Straße 569', 'Straße 569'),
    ('   AW: 569 Angebot', '569 Angebot')
]

for eingabe, sollwert in subject_cases:
    istwert = remove_prefixes(eingabe, TEST_PREFIX_LIST)
    assert istwert == sollwert, f'\n Eingabe: {eingabe!r} \n Ist: {istwert!r} \n Soll: {sollwert!r}'

# Test um das extrahieren der Projektnummern in extract_project_numbers zu prüfen

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
    assert istwert == sollwert, f'\n Eingabe: {eingabe!r} \n Ist: {istwert!r} \n Soll: {sollwert!r}'

# Test um die Überprüfung der Projektschwelle in check_project_number_threshold zu prüfen

project_number_threshold_cases = [
    ('501', True),
    ('500', True),
    ('1000', True),
    ('499', False),
    ('104', False)
]

for eingabe, sollwert in project_number_threshold_cases: 
    istwert = check_project_number_threshold(int(eingabe), TEST_PROJECT_NUMBER_THRESHOLD)
    assert istwert == sollwert, f'\n Eingabe: {eingabe!r} \n Ist: {istwert!r} \n Soll: {sollwert!r}'