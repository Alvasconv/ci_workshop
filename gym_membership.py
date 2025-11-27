"""
Gym Membership Management System
Miembro 1: Funcionalidad Base y Costos
- Requisito 1: Selección de Membresía
- Requisito 3: Cálculo de Costo Base y Total
- Requisito 7: Validación de Disponibilidad

Miembro 2: Características Adicionales y Descuentos
- Requisito 2: Características Adicionales
- Requisito 4: Descuentos por Grupo
- Requisito: Descuentos por Oferta Especial
"""

from discounts import MembershipCalculator

# Define available membership plans with their base costs
MEMBERSHIP_PLANS = {
    "basic": {
        "name": "Basic",
        "cost": 29.99,
        "description": "Access to gym facilities and basic equipment"
    },
    "premium": {
        "name": "Premium",
        "cost": 59.99,
        "description": "Access to gym facilities, group classes, and locker room"
    },
    "family": {
        "name": "Family",
        "cost": 99.99,
        "description": "Access for up to 4 family members with all basic amenities"
    }
}

# Define available additional features
ADDITIONAL_FEATURES = {
    "personal_training": {"name": "Personal Training Sessions", "cost": 50.00, "is_premium": False},
    "group_classes": {"name": "Group Classes", "cost": 20.00, "is_premium": False},
    "nutrition_coaching": {"name": "Nutrition Coaching", "cost": 30.00, "is_premium": False},
    "locker_room": {"name": "Premium Locker Room", "cost": 15.00, "is_premium": True}
}


def display_membership_plans():
    """
    Requirement 1: Display various gym membership plans with their benefits and costs.
    
    Returns:
        dict: A dictionary of available membership plans
    """
    print("\n=== Available Membership Plans ===")
    for key, plan in MEMBERSHIP_PLANS.items():
        print(f"{key.upper()}: ${plan['cost']:.2f}")
        print(f"  Description: {plan['description']}\n")
    return MEMBERSHIP_PLANS


def select_membership(plan_key):
    """
    Allow user to select a membership plan.
    
    Args:
        plan_key (str): The key of the selected membership plan (e.g., 'basic', 'premium')
    
    Returns:
        dict: Selected membership plan if valid, None otherwise
    """
    if plan_key.lower() not in MEMBERSHIP_PLANS:
        return None
    
    return MEMBERSHIP_PLANS[plan_key.lower()]


def validate_membership_availability(plan_key):
    """
    Requirement 7: Validate that the selected membership plan is available.
    
    Args:
        plan_key (str): The key of the membership plan to validate
    
    Returns:
        bool: True if available, False otherwise
    """
    return plan_key.lower() in MEMBERSHIP_PLANS


def validate_features_availability(feature_keys):
    """
    Requirement 7: Validate that selected additional features are available.
    
    Args:
        feature_keys (list): List of feature keys to validate
    
    Returns:
        tuple: (is_valid: bool, invalid_features: list)
    """
    invalid_features = []
    for feature_key in feature_keys:
        if feature_key.lower() not in ADDITIONAL_FEATURES:
            invalid_features.append(feature_key)
    
    return len(invalid_features) == 0, invalid_features


def calculate_base_membership_cost(plan_key):
    """
    Requirement 3: Determine the base cost for each selected membership plan.
    
    Args:
        plan_key (str): The key of the selected membership plan
    
    Returns:
        float: Base cost of membership, or -1 if plan is invalid
    """
    if not validate_membership_availability(plan_key):
        return -1
    
    return MEMBERSHIP_PLANS[plan_key.lower()]["cost"]


def calculate_additional_features_cost(feature_keys):
    """
    Requirement 3: Calculate the total cost of selected additional features.
    
    Args:
        feature_keys (list): List of feature keys to include
    
    Returns:
        tuple: (total_cost: float, invalid_features: list)
    """
    is_valid, invalid_features = validate_features_availability(feature_keys)
    
    if not is_valid:
        return -1, invalid_features
    
    total_cost = 0.0
    for feature_key in feature_keys:
        if feature_key.lower() in ADDITIONAL_FEATURES:
            total_cost += ADDITIONAL_FEATURES[feature_key.lower()]["cost"]
    
    return total_cost, []


def calculate_total_membership_cost(plan_key, feature_keys=None, num_people=1):
    """
    Requirement 3 & 4: Sum base membership cost and additional features cost to get total.
    Apply 10% discount if 2 or more people sign up.
    
    Args:
        plan_key (str): The key of the selected membership plan
        feature_keys (list): List of additional feature keys (default: empty list)
        num_people (int): Number of people signing up (default: 1)
    
    Returns:
        tuple: (total_cost: float, details: dict) or (-1, error_dict) if invalid
    """
    if feature_keys is None:
        feature_keys = []
    
    if num_people < 1:
        return -1, {"error": "Number of people must be at least 1"}
    
    # Validate membership plan
    if not validate_membership_availability(plan_key):
        return -1, {"error": f"Invalid membership plan: {plan_key}"}
    
    # Calculate base cost
    base_cost = calculate_base_membership_cost(plan_key)
    
    # Calculate features cost
    features_cost, invalid_features = calculate_additional_features_cost(feature_keys)
    
    if features_cost == -1:
        return -1, {"error": f"Invalid features: {invalid_features}"}
    
    # Prepare features for MembershipCalculator
    selected_features = select_additional_features(feature_keys)

    # Use MembershipCalculator for total calculation
    try:
        total_cost = MembershipCalculator.calculate_total(base_cost, selected_features, num_people)
    except ValueError as e:
        return -1, {"error": str(e)}
    
    details = {
        "membership_plan": MEMBERSHIP_PLANS[plan_key.lower()]["name"],
        "base_cost": base_cost,
        "features_cost": features_cost,
        "total_cost": total_cost,
        "features_selected": feature_keys,
        "num_people": num_people,
        "surcharge": 0.0, # Surcharge details are handled internally
        "discount": 0.0   # Discount details are handled internally
    }
    
    return total_cost, details


def get_membership_details(plan_key):
    """
    Get detailed information about a membership plan.
    
    Args:
        plan_key (str): The key of the membership plan
    
    Returns:
        dict: Membership details or None if invalid
    """
    if not validate_membership_availability(plan_key):
        return None
    
    return MEMBERSHIP_PLANS[plan_key.lower()]


def get_feature_details(feature_key):
    """
    Get detailed information about a feature.
    
    Args:
        feature_key (str): The key of the feature
    
    Returns:
        dict: Feature details or None if invalid
    """
    if feature_key.lower() not in ADDITIONAL_FEATURES:
        return None
    
    return ADDITIONAL_FEATURES[feature_key.lower()]


def display_additional_features():
    """
    Requirement 2: Display available additional features with their costs.
    
    Returns:
        dict: A dictionary of available additional features
    """
    print("\n=== Available Additional Features ===")
    for key, feature in ADDITIONAL_FEATURES.items():
        print(f"{key.upper()}: ${feature['cost']:.2f}")
        print(f"  Description: {feature['name']}\n")
    return ADDITIONAL_FEATURES


def select_additional_features(feature_keys):
    """
    Requirement 2: Allow user to select additional features.
    
    Args:
        feature_keys (list): List of feature keys to select
    
    Returns:
        list: List of selected feature dictionaries
    """
    selected_features = []
    for key in feature_keys:
        if key.lower() in ADDITIONAL_FEATURES:
            selected_features.append(ADDITIONAL_FEATURES[key.lower()])
    return selected_features
