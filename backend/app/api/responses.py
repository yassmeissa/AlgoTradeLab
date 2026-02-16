"""
Responses Documentation for Swagger/OpenAPI

Documenter les codes de réponse et les erreurs dans Swagger
"""

from fastapi import HTTPException, status
from typing import Dict, Any


# ============================================================================
# RÉPONSES HTTP STANDARDS
# ============================================================================

HTTP_RESPONSES = {
    200: {
        "description": "✅ Succès",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {"type": "object"}
                    }
                }
            }
        }
    },
    201: {
        "description": "✅ Créé avec succès",
    },
    204: {
        "description": "✅ Pas de contenu",
    },
    400: {
        "description": "❌ Requête invalide",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Invalid parameters"
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "❌ Non authentifié",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Not authenticated"
                        }
                    }
                }
            }
        }
    },
    403: {
        "description": "❌ Accès interdit",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Insufficient permissions"
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "❌ Ressource non trouvée",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Resource not found"
                        }
                    }
                }
            }
        }
    },
    422: {
        "description": "❌ Erreur de validation",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "loc": {"type": "array"},
                                    "msg": {"type": "string"},
                                    "type": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "❌ Erreur serveur interne",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Internal server error"
                        }
                    }
                }
            }
        }
    }
}


# ============================================================================
# EXEMPLE D'UTILISATION DANS LES ENDPOINTS
# ============================================================================

example_endpoint = """
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class StrategyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., description="mac, rsi, or macd")
    parameters: dict = Field(..., description="Strategy parameters")

@router.post(
    "/strategies",
    status_code=201,
    summary="Create Strategy",
    description="Create a new trading strategy",
    tags=["Strategies"],
    responses={
        201: {
            "description": "Strategy created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "My Strategy",
                        "type": "mac",
                        "created_at": "2024-01-15T10:30:00"
                    }
                }
            }
        },
        400: {
            "description": "Invalid strategy parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Strategy type must be one of: mac, rsi, macd"
                    }
                }
            }
        },
        401: {
            "description": "Authentication required"
        },
        422: {
            "description": "Validation error"
        }
    }
)
def create_strategy(
    strategy: StrategyCreate,
    token: str = Depends(verify_token)
):
    '''
    Create a new trading strategy.
    
    - **name**: Strategy name (required)
    - **type**: Strategy type: mac, rsi, or macd
    - **parameters**: Strategy-specific parameters
    
    Returns the created strategy with ID
    '''
    # Validation
    if strategy.type not in ["mac", "rsi", "macd"]:
        raise HTTPException(
            status_code=400,
            detail="Strategy type must be one of: mac, rsi, macd"
        )
    
    # Create strategy...
    return {"id": 1, "name": strategy.name, "type": strategy.type}
"""


# ============================================================================
# CODES D'ERREUR PERSONNALISÉS
# ============================================================================

class APIError(HTTPException):
    """Base class for API errors"""
    pass


class StrategyNotFoundError(APIError):
    """Strategy not found"""
    def __init__(self, strategy_id: int):
        super().__init__(
            status_code=404,
            detail=f"Strategy with ID {strategy_id} not found"
        )


class InvalidStrategyTypeError(APIError):
    """Invalid strategy type"""
    def __init__(self, strategy_type: str):
        super().__init__(
            status_code=400,
            detail=f"Invalid strategy type '{strategy_type}'. Must be: mac, rsi, macd"
        )


class InvalidParametersError(APIError):
    """Invalid parameters"""
    def __init__(self, message: str):
        super().__init__(
            status_code=422,
            detail=f"Invalid parameters: {message}"
        )


class AuthenticationError(APIError):
    """Authentication failed"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            status_code=401,
            detail=message
        )


class InsufficientPermissionsError(APIError):
    """User doesn't have permission"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            status_code=403,
            detail=message
        )


# ============================================================================
# UTILISATION DANS LES ENDPOINTS
# ============================================================================

example_usage = """
@router.get("/strategies/{strategy_id}", tags=["Strategies"])
def get_strategy(strategy_id: int, token: str = Depends(verify_token)):
    '''
    Get strategy by ID
    
    Raises:
        404: Strategy not found
        401: Not authenticated
    '''
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    
    if not strategy:
        raise StrategyNotFoundError(strategy_id)
    
    return strategy
"""


# ============================================================================
# DOCUMENTATION DES RÉPONSES D'ERREUR
# ============================================================================

error_response_doc = """
# Documentation des Codes de Réponse

## 2xx Success

### 200 OK
- Requête réussie
- La réponse contient les données demandées
- Exemple: GET /api/strategies/1

### 201 Created
- Ressource créée avec succès
- L'en-tête Location contient l'URI de la nouvelle ressource
- Exemple: POST /api/strategies

### 204 No Content
- Opération réussie
- Pas de contenu dans la réponse
- Exemple: DELETE /api/strategies/1

## 4xx Client Error

### 400 Bad Request
- Requête invalide
- Les paramètres sont malformés ou invalides
- Exemple: Invalid strategy type

### 401 Unauthorized
- Authentication requise
- Token manquant ou invalide
- Solution: Utiliser l'endpoint /auth/login

### 403 Forbidden
- L'utilisateur n'a pas la permission
- Exemple: Accès à une stratégie d'un autre utilisateur

### 404 Not Found
- Ressource non trouvée
- L'ID fourni n'existe pas
- Exemple: Stratégie avec ID 999

### 422 Unprocessable Entity
- Erreur de validation des données
- FastAPI retourne les détails des champs invalides
- Vérifier les types et formats des paramètres

## 5xx Server Error

### 500 Internal Server Error
- Erreur serveur
- Contacter le support avec l'ID de l'erreur
- Exemple: Erreur de base de données
"""


# ============================================================================
# RÉSUMÉ DES RÉPONSES
# ============================================================================

RESPONSES_SUMMARY = """
┌─────────────────────────────────────────────────┐
│         CODES DE RÉPONSE HTTP SWAGGER           │
├──────────┬─────────────────────────────────────┤
│ Code     │ Description                         │
├──────────┼─────────────────────────────────────┤
│ 200 ✅   │ Succès - Données retournées        │
│ 201 ✅   │ Créé - Ressource créée             │
│ 204 ✅   │ Pas de contenu - Succès silencieux │
│ 400 ❌   │ Requête invalide                   │
│ 401 ❌   │ Non authentifié                    │
│ 403 ❌   │ Accès interdit                     │
│ 404 ❌   │ Non trouvé                         │
│ 422 ❌   │ Erreur de validation               │
│ 500 ❌   │ Erreur serveur                     │
└──────────┴─────────────────────────────────────┘

Pour documenter dans Swagger, ajouter le paramètre
'responses' à chaque endpoint:

@router.get("/endpoint", responses=HTTP_RESPONSES)
def endpoint():
    pass
"""
