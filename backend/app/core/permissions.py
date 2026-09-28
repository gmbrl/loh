"""
Role definitions and permission helpers.

Every action in the system is gated by a permission check here.
Business logic lives in services/; this module only encodes *who* may do *what*.
"""

from enum import Enum
from typing import Set

from fastapi import HTTPException, status


class Role(str, Enum):
    ADMIN = "admin"
    SURVEYOR = "surveyor"
    CADASTRAL_OFFICER = "cadastral_officer"
    LAWYER_NOTARY = "lawyer_notary"
    REGISTRAR = "registrar"
    BANK = "bank"
    TAX_AUTHORITY = "tax_authority"
    COURT = "court"
    MUNICIPALITY = "municipality"
    CITIZEN = "citizen"


# ---------------------------------------------------------------------------
# Permission sets — maps (action, resource) → set of roles allowed
# ---------------------------------------------------------------------------

PERMISSIONS: dict[str, Set[Role]] = {
    # Parcels
    "parcel:submit_survey": {Role.SURVEYOR},
    "parcel:approve": {Role.CADASTRAL_OFFICER, Role.ADMIN},
    "parcel:reject": {Role.CADASTRAL_OFFICER, Role.ADMIN},
    "parcel:read_public": set(Role),  # all roles
    "parcel:read_detail": {
        Role.ADMIN,
        Role.CADASTRAL_OFFICER,
        Role.REGISTRAR,
        Role.SURVEYOR,
        Role.LAWYER_NOTARY,
        Role.COURT,
    },
    # Titles
    "title:initiate": {Role.CITIZEN, Role.LAWYER_NOTARY, Role.ADMIN},
    "title:prepare_instrument": {Role.LAWYER_NOTARY, Role.ADMIN},
    "title:submit": {Role.LAWYER_NOTARY, Role.CITIZEN, Role.ADMIN},
    "title:approve": {Role.REGISTRAR, Role.ADMIN},
    "title:reject": {Role.REGISTRAR, Role.ADMIN},
    "title:read_public": set(Role),
    "title:read_full": {
        Role.REGISTRAR,
        Role.ADMIN,
        Role.LAWYER_NOTARY,
        Role.COURT,
        # owner check is enforced at the service layer
    },
    # Encumbrances
    "encumbrance:submit_mortgage": {Role.BANK, Role.ADMIN},
    "encumbrance:submit_tax_lien": {Role.TAX_AUTHORITY, Role.ADMIN},
    "encumbrance:submit_court_order": {Role.COURT, Role.ADMIN},
    "encumbrance:submit_municipal": {Role.MUNICIPALITY, Role.ADMIN},
    "encumbrance:submit_private": {Role.LAWYER_NOTARY, Role.CITIZEN, Role.ADMIN},
    "encumbrance:release": {
        Role.BANK,
        Role.TAX_AUTHORITY,
        Role.COURT,
        Role.MUNICIPALITY,
        Role.REGISTRAR,
        Role.ADMIN,
    },
    "encumbrance:approve": {Role.REGISTRAR, Role.ADMIN},
    "encumbrance:read_public": set(Role),
    # Corrections
    "correction:submit_clerical": {
        Role.CADASTRAL_OFFICER,
        Role.REGISTRAR,
        Role.ADMIN,
    },
    "correction:submit_technical": {
        Role.SURVEYOR,
        Role.CADASTRAL_OFFICER,
        Role.ADMIN,
    },
    "correction:submit_substantive": {Role.COURT, Role.ADMIN},
    "correction:approve": {Role.CADASTRAL_OFFICER, Role.REGISTRAR, Role.ADMIN},
    "correction:read": {
        Role.ADMIN,
        Role.CADASTRAL_OFFICER,
        Role.REGISTRAR,
        Role.SURVEYOR,
        Role.COURT,
        Role.LAWYER_NOTARY,
    },
    # Admin
    "user:manage": {Role.ADMIN},
}


def require_permission(user_role: str, permission: str) -> None:
    """Raise HTTP 403 if the role does not have the required permission."""
    allowed: Set[Role] = PERMISSIONS.get(permission, set())
    try:
        role = Role(user_role)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unknown role")
    if role not in allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{user_role}' does not have permission '{permission}'",
        )
