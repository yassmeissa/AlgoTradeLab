#!/bin/bash

# ============================================================================
# AlgoTrade Lab - Swagger Demo Script
# ============================================================================
# 
# Ce script démontre comment utiliser Swagger avec AlgoTrade Lab
#
# Usage:
#   ./swagger_demo.sh start      - Démarrer le serveur
#   ./swagger_demo.sh test       - Tester Swagger
#   ./swagger_demo.sh clean      - Nettoyer
#
# ============================================================================

set -e

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_DIR="$SCRIPT_DIR/backend/venv"

# ============================================================================
# Fonctions utilitaires
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# ============================================================================
# Installation des dépendances
# ============================================================================

setup_environment() {
    print_header "Installation de l'environnement"
    
    cd "$BACKEND_DIR"
    
    # Vérifier si Python 3 est installé
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 n'est pas installé"
        exit 1
    fi
    
    print_info "Python trouvé: $(python3 --version)"
    
    # Créer l'environnement virtuel
    if [ ! -d "$VENV_DIR" ]; then
        print_info "Création de l'environnement virtuel..."
        python3 -m venv venv
        print_success "Environnement virtuel créé"
    else
        print_info "Environnement virtuel existant"
    fi
    
    # Activer l'environnement
    source "$VENV_DIR/bin/activate"
    
    # Installer les dépendances
    print_info "Installation des dépendances..."
    pip install -q --upgrade pip
    
    if [ -f "requirements.txt" ]; then
        pip install -q -r requirements.txt
        print_success "Dépendances installées"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# ============================================================================
# Démarrer le serveur
# ============================================================================

start_server() {
    print_header "Démarrage du serveur Swagger"
    
    cd "$BACKEND_DIR"
    source "$VENV_DIR/bin/activate"
    
    print_info "Serveur démarrant sur http://localhost:8000"
    echo ""
    print_info "Accès à Swagger UI:"
    echo -e "  ${YELLOW}http://localhost:8000/docs${NC}"
    echo ""
    print_info "Accès à ReDoc:"
    echo -e "  ${YELLOW}http://localhost:8000/redoc${NC}"
    echo ""
    print_info "Schéma OpenAPI JSON:"
    echo -e "  ${YELLOW}http://localhost:8000/openapi.json${NC}"
    echo ""
    print_info "Appuyez sur Ctrl+C pour arrêter le serveur"
    echo ""
    
    python run.py
}

# ============================================================================
# Tester Swagger
# ============================================================================

test_swagger() {
    print_header "Test de Swagger"
    
    # Vérifier si le serveur est en cours d'exécution
    print_info "Vérification du serveur..."
    
    if curl -s http://localhost:8000/openapi.json > /dev/null 2>&1; then
        print_success "Serveur accessible"
    else
        print_error "Le serveur n'est pas accessible"
        print_info "Assurez-vous que le serveur est démarré avec: ./swagger_demo.sh start"
        exit 1
    fi
    
    # Récupérer le schéma OpenAPI
    print_info "Récupération du schéma OpenAPI..."
    SCHEMA=$(curl -s http://localhost:8000/openapi.json)
    
    # Extraire les informations
    TITLE=$(echo "$SCHEMA" | grep -o '"title":"[^"]*' | cut -d'"' -f4)
    VERSION=$(echo "$SCHEMA" | grep -o '"version":"[^"]*' | cut -d'"' -f4)
    
    print_success "OpenAPI Schema OK"
    echo "  Title:   $TITLE"
    echo "  Version: $VERSION"
    echo ""
    
    # Tester les endpoints
    print_info "Test des endpoints Swagger..."
    
    echo -e "  ${YELLOW}GET /docs${NC}           - Swagger UI"
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep -q "200"; then
        echo -e "    ${GREEN}✓ Accessible${NC}"
    else
        echo -e "    ${RED}✗ Non accessible${NC}"
    fi
    
    echo -e "  ${YELLOW}GET /redoc${NC}          - ReDoc"
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/redoc | grep -q "200"; then
        echo -e "    ${GREEN}✓ Accessible${NC}"
    else
        echo -e "    ${RED}✗ Non accessible${NC}"
    fi
    
    echo -e "  ${YELLOW}GET /openapi.json${NC}   - OpenAPI Schema"
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/openapi.json | grep -q "200"; then
        echo -e "    ${GREEN}✓ Accessible${NC}"
    else
        echo -e "    ${RED}✗ Non accessible${NC}"
    fi
    
    echo ""
    print_success "Tous les tests Swagger sont passés!"
}

# ============================================================================
# Ouvrir Swagger dans le navigateur
# ============================================================================

open_swagger() {
    print_header "Ouverture de Swagger UI"
    
    print_info "Vérification du serveur..."
    if ! curl -s http://localhost:8000/openapi.json > /dev/null 2>&1; then
        print_error "Le serveur n'est pas accessible"
        exit 1
    fi
    
    print_success "Serveur accessible"
    print_info "Ouverture du navigateur..."
    
    # Déterminer le navigateur par défaut en fonction du système d'exploitation
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "http://localhost:8000/docs"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "http://localhost:8000/docs"
    elif [[ "$OSTYPE" == "msys" ]]; then
        start "http://localhost:8000/docs"
    fi
}

# ============================================================================
# Afficher les informations
# ============================================================================

show_info() {
    print_header "AlgoTrade Lab - Swagger Info"
    
    echo "Commandes disponibles:"
    echo ""
    echo -e "  ${YELLOW}./swagger_demo.sh setup${NC}   - Installation"
    echo -e "  ${YELLOW}./swagger_demo.sh start${NC}   - Démarrer le serveur"
    echo -e "  ${YELLOW}./swagger_demo.sh test${NC}    - Tester Swagger"
    echo -e "  ${YELLOW}./swagger_demo.sh open${NC}    - Ouvrir Swagger UI"
    echo -e "  ${YELLOW}./swagger_demo.sh info${NC}    - Afficher cette aide"
    echo ""
    
    echo "URLs principales:"
    echo ""
    echo -e "  ${BLUE}Swagger UI:${NC}"
    echo -e "    http://localhost:8000/docs"
    echo ""
    echo -e "  ${BLUE}ReDoc Documentation:${NC}"
    echo -e "    http://localhost:8000/redoc"
    echo ""
    echo -e "  ${BLUE}OpenAPI JSON Schema:${NC}"
    echo -e "    http://localhost:8000/openapi.json"
    echo ""
}

# ============================================================================
# Nettoyer
# ============================================================================

clean() {
    print_header "Nettoyage"
    
    print_info "Suppression de l'environnement virtuel..."
    rm -rf "$VENV_DIR"
    print_success "Environnement virtuel supprimé"
    
    print_info "Suppression des fichiers __pycache__..."
    find "$BACKEND_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    print_success "Cache Python supprimé"
}

# ============================================================================
# Main
# ============================================================================

main() {
    case "${1:-info}" in
        setup)
            setup_environment
            ;;
        start)
            setup_environment
            start_server
            ;;
        test)
            test_swagger
            ;;
        open)
            open_swagger
            ;;
        info|--help|-h)
            show_info
            ;;
        clean)
            clean
            ;;
        *)
            print_error "Commande inconnue: $1"
            show_info
            exit 1
            ;;
    esac
}

# Exécuter main
main "$@"
