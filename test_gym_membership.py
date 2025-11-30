"""
Unit tests for Gym Membership Management System
Tests for Miembro 1 functionality:
- Requirement 1: Membership Selection
- Requirement 3: Cost Calculation
- Requirement 7: Availability Validation
"""

import pytest

from gym_membership import (ADDITIONAL_FEATURES, MEMBERSHIP_PLANS,
                            calculate_additional_features_cost,
                            calculate_base_membership_cost,
                            calculate_total_membership_cost,
                            display_membership_plans, get_feature_details,
                            get_membership_details, select_membership,
                            validate_features_availability,
                            validate_membership_availability)


class TestMembershipSelection:
    """Tests for Requirement 1: Membership Selection"""

    def test_display_membership_plans(self):
        """Test that membership plans are displayed correctly"""
        plans = display_membership_plans()
        assert isinstance(plans, dict)
        assert len(plans) == 3
        assert "basic" in plans
        assert "premium" in plans
        assert "family" in plans

    def test_select_valid_membership(self):
        """Test selecting a valid membership plan"""
        membership = select_membership("basic")
        assert membership is not None
        assert membership["name"] == "Basic"
        assert membership["cost"] == 29.99

    def test_select_membership_case_insensitive(self):
        """Test that membership selection is case insensitive"""
        membership1 = select_membership("PREMIUM")
        membership2 = select_membership("premium")
        assert membership1 == membership2

    def test_select_invalid_membership(self):
        """Test selecting an invalid membership plan"""
        membership = select_membership("gold")
        assert membership is None

    def test_get_membership_details(self):
        """Test retrieving membership details"""
        details = get_membership_details("family")
        assert details is not None
        assert details["cost"] == 99.99


class TestAvailabilityValidation:
    """Tests for Requirement 7: Availability Validation"""

    def test_validate_valid_membership(self):
        """Test validation of a valid membership plan"""
        is_valid = validate_membership_availability("basic")
        assert is_valid is True

    def test_validate_invalid_membership(self):
        """Test validation of an invalid membership plan"""
        is_valid = validate_membership_availability("platinum")
        assert is_valid is False

    def test_validate_valid_features(self):
        """Test validation of valid features"""
        is_valid, invalid = validate_features_availability(
            ["personal_training", "group_classes"]
        )
        assert is_valid is True
        assert len(invalid) == 0

    def test_validate_invalid_features(self):
        """Test validation with invalid features"""
        is_valid, invalid = validate_features_availability(
            ["personal_training", "invalid_feature"]
        )
        assert is_valid is False
        assert "invalid_feature" in invalid

    def test_validate_empty_features_list(self):
        """Test validation of empty features list"""
        is_valid, invalid = validate_features_availability([])
        assert is_valid is True
        assert len(invalid) == 0


class TestCostCalculation:
    """Tests for Requirement 3: Cost Calculation"""

    def test_calculate_base_cost_basic(self):
        """Test calculating base cost for basic membership"""
        cost = calculate_base_membership_cost("basic")
        assert cost == 29.99

    def test_calculate_base_cost_premium(self):
        """Test calculating base cost for premium membership"""
        cost = calculate_base_membership_cost("premium")
        assert cost == 59.99

    def test_calculate_base_cost_family(self):
        """Test calculating base cost for family membership"""
        cost = calculate_base_membership_cost("family")
        assert cost == 99.99

    def test_calculate_base_cost_invalid(self):
        """Test calculating base cost for invalid membership returns -1"""
        cost = calculate_base_membership_cost("invalid")
        assert cost == -1

    def test_calculate_features_cost_single(self):
        """Test calculating cost of a single feature"""
        cost, invalid = calculate_additional_features_cost(["personal_training"])
        assert cost == 50.00
        assert len(invalid) == 0

    def test_calculate_features_cost_multiple(self):
        """Test calculating cost of multiple features"""
        cost, invalid = calculate_additional_features_cost(
            ["personal_training", "group_classes"]
        )
        assert cost == 70.00
        assert len(invalid) == 0

    def test_calculate_features_cost_invalid(self):
        """Test calculating cost with invalid features"""
        cost, invalid = calculate_additional_features_cost(
            ["personal_training", "invalid"]
        )
        assert cost == -1
        assert "invalid" in invalid

    def test_calculate_features_cost_empty(self):
        """Test calculating cost with no features"""
        cost, invalid = calculate_additional_features_cost([])
        assert cost == 0.00
        assert len(invalid) == 0

    def test_calculate_total_cost_basic_no_features(self):
        """Test total cost for basic membership without features"""
        total, details = calculate_total_membership_cost("basic")
        assert total == 29.99
        assert details["membership_plan"] == "Basic"
        assert details["base_cost"] == 29.99
        assert details["features_cost"] == 0.0

    def test_calculate_total_cost_with_features(self):
        """Test total cost with membership and features"""
        total, details = calculate_total_membership_cost(
            "premium", ["personal_training", "nutrition_coaching"]
        )
        expected_total = 59.99 + 50.00 + 30.00
        assert total == expected_total
        assert details["membership_plan"] == "Premium"
        assert details["base_cost"] == 59.99
        assert details["features_cost"] == 80.00

    def test_calculate_total_cost_invalid_membership(self):
        """Test total cost with invalid membership"""
        total, details = calculate_total_membership_cost("invalid")
        assert total == -1
        assert "error" in details

    def test_calculate_total_cost_invalid_features(self):
        """Test total cost with invalid features"""
        total, details = calculate_total_membership_cost("basic", ["invalid_feature"])
        assert total == -1
        assert "error" in details

    def test_calculate_total_cost_family_with_all_features(self):
        """Test total cost for family membership with all features"""
        all_features = list(ADDITIONAL_FEATURES.keys())
        total, details = calculate_total_membership_cost("family", all_features)
        expected_features_cost = sum(f["cost"] for f in ADDITIONAL_FEATURES.values())
        expected_total = 99.99 + expected_features_cost

        # Apply premium surcharge if applicable
        has_premium = any(
            f.get("is_premium", False) for f in ADDITIONAL_FEATURES.values()
        )
        if has_premium:
            expected_total += expected_total * 0.15

        # Apply special offer discount if applicable
        if expected_total > 400:
            expected_total -= 50.00
        elif expected_total > 200:
            expected_total -= 20.00

        assert total == pytest.approx(expected_total, 0.01)


class TestEdgeCases:
    """Tests for edge cases and error handling"""

    def test_case_insensitivity_for_features(self):
        """Test that feature keys are case insensitive"""
        cost1, _ = calculate_additional_features_cost(["PERSONAL_TRAINING"])
        cost2, _ = calculate_additional_features_cost(["personal_training"])
        assert cost1 == cost2

    def test_get_feature_details_valid(self):
        """Test retrieving valid feature details"""
        details = get_feature_details("personal_training")
        assert details is not None
        assert details["cost"] == 50.00

    def test_get_feature_details_invalid(self):
        """Test retrieving invalid feature details"""
        details = get_feature_details("invalid")
        assert details is None

    def test_duplicate_features(self):
        """Test handling of duplicate features in selection"""
        cost, invalid = calculate_additional_features_cost(
            ["personal_training", "personal_training"]
        )
        assert cost == 100.00  # Both instances counted
        assert len(invalid) == 0

    def test_empty_membership_plan_key(self):
        """Test handling of empty membership plan key"""
        is_valid = validate_membership_availability("")
        assert is_valid is False

    def test_none_features_in_total_cost(self):
        """Test that None features defaults to empty list"""
        total1, _ = calculate_total_membership_cost("basic", None)
        total2, _ = calculate_total_membership_cost("basic", [])
        assert total1 == total2


class TestPricingAccuracy:
    """Tests to verify pricing calculations are accurate"""

    def test_total_cost_accuracy(self):
        """Test that total cost equals base + features exactly"""
        plan_key = "premium"
        features = ["personal_training", "nutrition_coaching"]

        base_cost = calculate_base_membership_cost(plan_key)
        features_cost, _ = calculate_additional_features_cost(features)
        total_cost, details = calculate_total_membership_cost(plan_key, features)

        assert total_cost == base_cost + features_cost
        assert details["base_cost"] == base_cost
        assert details["features_cost"] == features_cost

    def test_all_membership_costs_are_positive(self):
        """Test that all membership base costs are positive"""
        for plan in MEMBERSHIP_PLANS.values():
            assert plan["cost"] > 0

    def test_all_feature_costs_are_positive(self):
        """Test that all feature costs are positive"""
        for feature in ADDITIONAL_FEATURES.values():
            assert feature["cost"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
