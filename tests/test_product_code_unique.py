# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from decimal import Decimal
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction


class TestCase(unittest.TestCase):
    'Test module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('product_code_unique')
        self.template = POOL.get('product.template')
        self.uom = POOL.get('product.uom')

    def test0010check_uniqueness(self):
        'Test check uniqueness'
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            kilogram, = self.uom.search([
                    ('name', '=', 'Kilogram'),
                    ], limit=1)
            self.template.create([{
                        'name': 'P1',
                        'type': 'goods',
                        'list_price': Decimal(20),
                        'cost_price': Decimal(10),
                        'default_uom': kilogram.id,
                        'products': [('create', [{
                                        'code': '1',
                                        }])],
                        }])

            # Don't fail if no code
            self.template.create([{
                        'name': 'P2',
                        'type': 'goods',
                        'list_price': Decimal(20),
                        'cost_price': Decimal(10),
                        'default_uom': kilogram.id,
                        'products': [('create', [{}])],
                        }])

            # Fail if repeated code
            self.assertRaises(Exception, self.template.create, [{
                        'name': 'P3',
                        'type': 'goods',
                        'list_price': Decimal(20),
                        'cost_price': Decimal(10),
                        'default_uom': kilogram.id,
                        'products': [('create', [{
                                        'code': '1',
                                        }])],
                        }])
            transaction.cursor.rollback()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
