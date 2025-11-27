"""
Module for calculating membership costs and applying discounts.
This module contains the business logic for:
- Requirement 2: Additional Features
- Requirement 6: Premium Surcharge
- Requirement 4: Group Discounts
- Requirement 5: Special Offer Discounts
"""

from typing import List, Dict, Any, Union

class MembershipCalculator:
    """
    Calculator for gym membership costs including features, surcharges, and discounts.
    """

    @staticmethod
    def calculate_total(base_cost: float, features: List[Dict[str, Any]], num_people: int = 1) -> float:
        """
        Calculate the final total cost applying all business rules.

        Args:
            base_cost (float): The base cost of the membership plan.
            features (list): List of dictionaries representing selected features.
                             Each dict must have 'cost' (float) and optionally 'is_premium' (bool).
            num_people (int): Number of people signing up. Default is 1.

        Returns:
            float: The final calculated cost.
            
        Raises:
            ValueError: If inputs are invalid (negative costs, less than 1 person).
        """
        # Input Validation
        if base_cost < 0:
            raise ValueError("Base cost cannot be negative.")
        if num_people < 1:
            raise ValueError("Number of people must be at least 1.")
        
        features_cost = 0.0
        has_premium = False

        for feature in features:
            cost = feature.get("cost", 0.0)
            if cost < 0:
                raise ValueError("Feature cost cannot be negative.")
            features_cost += cost
            
            if feature.get("is_premium", False):
                has_premium = True

        # Step 1: Base + Features
        subtotal_per_person = base_cost + features_cost

        # Step 2: Requirement 6 - Premium Surcharge (15%)
        if has_premium:
            subtotal_per_person *= 1.15

        # Step 3: Calculate total for the group
        total_accumulated = subtotal_per_person * num_people

        # Step 4: Requirement 4 - Group Discount (10% if 2+ people)
        if num_people >= 2:
            total_accumulated *= 0.90

        # Step 5: Requirement 5 - Special Offer Discounts
        # If total > 400, subtract 50
        # If total > 200 (and <= 400), subtract 20
        if total_accumulated > 400:
            total_accumulated -= 50.00
        elif total_accumulated > 200:
            total_accumulated -= 20.00

        # Round to 2 decimal places for currency
        return round(total_accumulated, 2)
