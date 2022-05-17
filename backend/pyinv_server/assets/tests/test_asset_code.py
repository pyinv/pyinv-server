from assets.asset_codes import Damm32AssetCodeStrategy
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestDamm32AssetCode(TestCase):

    VALID_CODES = ['INV-DRE-XY2', 'INV-ZI3-T5X', 'INV-JRU-NXQ', 'INV-JGK-YT7', 'INV-NOZ-RDX', 'INV-IQB-6AR', 'INV-MI5-5SK', 'INV-KUD-LHR', 'INV-J47-G7V', 'INV-Q7A-6VK']  # noqa: E501
    INVALID_CODES = ['INV-DRE-XYZ', 'INV-IZ3-T5X', 'SOR-JRU-NX2', 'INVDDDD-JGK-YT7', 'INVOZ-RDX', 'INV-1QB-6AR', 'INV-MI5-SSK', 'INVKUD-LHR', 'INV-J47-V', 'INV-Q7A-6V']  # noqa: E501

    def setUp(self):
        self.strategy = Damm32AssetCodeStrategy()

    def test_generate_and_validate_asset_codes(self):
        for _ in range(100):
            code = self.strategy.generate_new_code()
            self.strategy.validate(code)

    def test_validate_good_asset_codes(self):
        for code in self.VALID_CODES:
            self.strategy.validate(code)

    def test_validate_bad_asset_codes(self):
        for code in self.INVALID_CODES:
            with self.assertRaises(ValidationError):
                self.strategy.validate(code)
