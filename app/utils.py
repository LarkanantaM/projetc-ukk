def get_jurusan_name(code):
    jurusan_names = {
        'RPL': 'Rekayasa Perangkat Lunak',
        'TSM': 'Teknik Sepeda Motor',
        'HOTEL': 'Perhotelan'
    }
    return jurusan_names.get(code, code)