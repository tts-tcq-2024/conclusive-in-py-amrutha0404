import unittest
from unittest.mock import patch
from typewise_alert import (
    classify_temperature_breach,
    check_and_alert,
    cooling_strategy_factory,
    alert_strategy_factory,
    PassiveCooling,
    HiActiveCooling,
    MedActiveCooling
)

class TypewiseAlertTest(unittest.TestCase):
    def test_classify_temperature_breach_passive_cooling(self):
        cooling_strategy = PassiveCooling()
        self.assertEqual(classify_temperature_breach(cooling_strategy, 25), 'NORMAL')

    def test_classify_temperature_breach_hi_active_cooling(self):
        cooling_strategy = HiActiveCooling()
        self.assertEqual(classify_temperature_breach(cooling_strategy, 46), 'TOO_HIGH')

    def test_classify_temperature_breach_med_active_cooling(self):
        cooling_strategy = MedActiveCooling()
        self.assertEqual(classify_temperature_breach(cooling_strategy, -1), 'TOO_LOW')

    @patch('typewise_alert.ControllerAlert.send_alert')
    def test_check_and_alert_controller(self, mock_send_alert):
        cooling_strategy = cooling_strategy_factory('PASSIVE_COOLING')
        alert_strategy = alert_strategy_factory('TO_CONTROLLER')
        check_and_alert(alert_strategy, cooling_strategy, 30)
        mock_send_alert.assert_called_once_with('NORMAL')

    @patch('typewise_alert.EmailAlert.send_alert')
    def test_check_and_alert_email_high(self, mock_send_alert):
        cooling_strategy = cooling_strategy_factory('HI_ACTIVE_COOLING')
        alert_strategy = alert_strategy_factory('TO_EMAIL')
        check_and_alert(alert_strategy, cooling_strategy, 50)
        mock_send_alert.assert_called_once_with('TOO_HIGH')

    @patch('typewise_alert.EmailAlert.send_alert')
    def test_check_and_alert_email_low(self, mock_send_alert):
        cooling_strategy = cooling_strategy_factory('MED_ACTIVE_COOLING')
        alert_strategy = alert_strategy_factory('TO_EMAIL')
        check_and_alert(alert_strategy, cooling_strategy, -5)
        mock_send_alert.assert_called_once_with('TOO_LOW')

if __name__ == '__main__':
    unittest.main()
