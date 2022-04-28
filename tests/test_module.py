
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.transaction import Transaction
from trytond.pool import Pool


class ProductCodeUniqueTestCase(ModuleTestCase):
    'Test ProductCodeUnique module'
    module = 'product_code_unique'

    @with_transaction()
    def test0010check_uniqueness(self):
        'Test check uniqueness'
        pool = Pool()
        Template = pool.get('product.template')
        Uom = pool.get('product.uom')
        transaction = Transaction()

        kilogram, = Uom.search([
                ('name', '=', 'Kilogram'),
                ], limit=1)
        Template.create([{
                    'name': 'P1',
                    'type': 'goods',
                    'default_uom': kilogram.id,
                    'products': [('create', [{
                                    'code': '1',
                                    }])],
                    }])

        # Don't fail if no code
        Template.create([{
                    'name': 'P2',
                    'type': 'goods',
                    'default_uom': kilogram.id,
                    'products': [('create', [{}])],
                    }])

        # Fail if repeated code
        self.assertRaises(Exception, Template.create([{
                    'name': 'P3',
                    'type': 'goods',
                    'default_uom': kilogram.id,
                    'products': [('create', [{
                                    'code': '1',
                                    }])],
                    }]))
        transaction.rollback()


del ModuleTestCase
