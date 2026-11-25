def find_test_mail(items, subject_prefix):
    for item in items:
        if item.Subject.startswith(subject_prefix):
            return item
    raise ValueError(f'Keine Testmail mit Betreff-Präfix {subject_prefix!r} gefunden.')