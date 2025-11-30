"""
Unit tests for MembershipCalculator logic.
Covers Requirements 2, 4, 5, and 6.
"""

import pytest

from discounts import MembershipCalculator


class TestMembershipCalculator:
    """Test suite for MembershipCalculator class"""

    def test_basic_calculation_no_features(self):
        """Test calculation with only base cost, 1 person"""
        # 100 base -> 100 total
        total = MembershipCalculator.calculate_total(100.0, [], 1)
        assert total == 100.0

    def test_sum_features(self):
        """Test Requirement 2: Sum of additional features"""
        # 100 base + 20 feature + 30 feature = 150
        features = [
            {"cost": 20.0, "is_premium": False},
            {"cost": 30.0, "is_premium": False},
        ]
        total = MembershipCalculator.calculate_total(100.0, features, 1)
        assert total == 150.0

    def test_premium_surcharge(self):
        """Test Requirement 6: 15% surcharge for premium features"""
        # Base 100 + Premium Feature 50 = 150
        # Surcharge 15% of 150 = 22.5
        # Total = 172.5
        features = [{"cost": 50.0, "is_premium": True}]
        total = MembershipCalculator.calculate_total(100.0, features, 1)
        assert total == 172.5

    def test_group_discount(self):
        """Test Requirement 4: 10% discount for 2+ people"""
        # Base 100. 2 People.
        # Subtotal = 200.
        # Discount 10% = 20.
        # Total = 180.
        total = MembershipCalculator.calculate_total(100.0, [], 2)
        assert total == 180.0

    def test_special_offer_20(self):
        """Test Requirement 5: $20 discount for total > 200"""
        # Base 250. 1 Person.
        # Total > 200 -> 250 - 20 = 230.
        total = MembershipCalculator.calculate_total(250.0, [], 1)
        assert total == 230.0

    def test_special_offer_50(self):
        """Test Requirement 5: $50 discount for total > 400"""
        # Base 500. 1 Person.
        # Total > 400 -> 500 - 50 = 450.
        total = MembershipCalculator.calculate_total(500.0, [], 1)
        assert total == 450.0

    def test_combination_all_rules(self):
        """Test combination: Group + Premium + Special Offer"""
        # Base 100.
        # Feature 50 (Premium).
        # Subtotal per person = (100 + 50) * 1.15 = 172.5
        # 3 People.
        # Group Total = 172.5 * 3 = 517.5
        # Group Discount 10% = 517.5 * 0.90 = 465.75
        # Special Offer (>400) = 465.75 - 50 = 415.75

        features = [{"cost": 50.0, "is_premium": True}]
        total = MembershipCalculator.calculate_total(100.0, features, 3)
        assert total == 415.75

    def test_invalid_inputs(self):
        """Test error handling for invalid inputs"""
        with pytest.raises(ValueError):
            MembershipCalculator.calculate_total(-100.0, [], 1)

        with pytest.raises(ValueError):
            MembershipCalculator.calculate_total(100.0, [], 0)

        with pytest.raises(ValueError):
            MembershipCalculator.calculate_total(100.0, [{"cost": -10.0}], 1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
