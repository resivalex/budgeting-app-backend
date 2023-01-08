class Example:

    def all(self):
        return [
            {
                'datetime': '2023-01-06 09:59:59',
                'account': 'Russian bank',
                'category': 'Correction',
                'type': 'income',
                'amount': '3000.00',
                'currency': 'RUB',
                'payee': '',
                'comment': 'Initial balance'
            },
            {
                'datetime': '2023-01-07 10:00:00',
                'account': 'Cash',
                'category': 'Correction',
                'type': 'income',
                'amount': '10000.00',
                'currency': 'KZT',
                'payee': '',
                'comment': 'Initial balance'
            },
            {
                'datetime': '2023-01-07 10:07:30',
                'account': 'Cash',
                'category': '',
                'type': 'transfer',
                'amount': '5000.00',
                'currency': 'KZT',
                'payee': 'Bank card',
                'comment': 'Initial balance'
            },
            {
                'datetime': '2023-01-08 12:13:14',
                'account': 'Bank card',
                'category': 'Fastfood',
                'type': 'expense',
                'amount': '1950.00',
                'currency': 'KZT',
                'payee': 'KFC',
                'comment': 'Basket'
            }
        ]
