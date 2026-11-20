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
    uppercase_subject = subject.upper()
    uppercase_prefix_list = [prefix.upper() for prefix in prefix_list]
    flag = True

    while flag:
        flag = False
        for prefix in uppercase_prefix_list:
            if uppercase_subject.startswith(prefix):
                uppercase_subject = uppercase_subject.removeprefix(prefix)
                uppercase_subject = uppercase_subject.lstrip()
                flag = True
                # print(prefix, flag, uppercase_subject)  

    length = len(subject) - len(uppercase_subject)

    adjusted_subject = subject[length:]

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