data = {
    'Giant Spider': {
        '10E': {
            'release_date': '2000',
            'printings': {
                'second': {
                    'number': 2,
                },
                'first': {
                    'number': 1,
                },
            }
        },
        'LEA': {
            'release_date': '1993',
            'printings': {
                'second': {
                    'number': 2,
                },
                'first': {
                    'number': 1,
                },
            }
        },
    },
    'Atog': {
        '10E': {
            'release_date': '2000',
            'printings': {
                'second': {
                    'number': 2,
                },
                'first': {
                    'number': 1,
                },
            }
        },
        'LEA': {
            'release_date': '1993',
            'printings': {
                'second': {
                    'number': 2,
                },
                'first': {
                    'number': 1,
                },
            }
        }
    },
}


print(data)

print('\n')

print(
    sorted(
        data.items(), key=lambda kv: kv[0]
    )
)
