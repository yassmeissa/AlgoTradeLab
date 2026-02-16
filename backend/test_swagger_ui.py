#!/usr/bin/env python3
"""
Test Script for Swagger UI Validation

Vérifie que Swagger est correctement configuré et accessible
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path


def test_swagger_endpoints():
    """
    Test les différents endpoints de Swagger
    """
    base_url = "http://localhost:8000"
    
    print("=" * 80)
    print("🧪 TEST SWAGGER UI - Validation des Endpoints")
    print("=" * 80)
    print()
    
    # Test 1: OpenAPI Schema
    print("1️⃣  Récupération du schéma OpenAPI...")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        if response.status_code == 200:
            schema = response.json()
            print(f"   ✅ Schéma OpenAPI accessible")
            print(f"   📝 Title: {schema.get('info', {}).get('title')}")
            print(f"   📝 Version: {schema.get('info', {}).get('version')}")
            print(f"   📝 Endpoints trouvés: {len(schema.get('paths', {}))}")
            print()
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    # Test 2: Swagger UI
    print("2️⃣  Vérification de Swagger UI...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Swagger UI accessible à /docs")
            print()
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    # Test 3: ReDoc
    print("3️⃣  Vérification de ReDoc...")
    try:
        response = requests.get(f"{base_url}/redoc", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ ReDoc accessible à /redoc")
            print()
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    # Test 4: Endpoints Details
    print("4️⃣  Analyse des Endpoints...")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        schema = response.json()
        paths = schema.get('paths', {})
        
        print(f"   Endpoints trouvés ({len(paths)}):")
        for path, methods in sorted(paths.items())[:10]:  # Show first 10
            for method in methods.keys():
                if method not in ['parameters', 'summary']:
                    op = methods[method]
                    summary = op.get('summary', 'No summary')
                    print(f"   • {method.upper():6} {path:30} - {summary}")
        
        if len(paths) > 10:
            print(f"   ... et {len(paths) - 10} autres endpoints")
        print()
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    # Test 5: Tags Metadata
    print("5️⃣  Vérification des Tags...")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        schema = response.json()
        tags = schema.get('tags', [])
        
        if tags:
            print(f"   ✅ Tags trouvés ({len(tags)}):")
            for tag in tags:
                print(f"   • {tag.get('name'):15} - {tag.get('description', 'No description')}")
            print()
        else:
            print(f"   ℹ️  Aucun tag configuré (optionnel)")
            print()
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    return True


def validate_openapi_schema():
    """
    Valide le schéma OpenAPI
    """
    print("=" * 80)
    print("🔍 VALIDATION DU SCHÉMA OPENAPI")
    print("=" * 80)
    print()
    
    try:
        base_url = "http://localhost:8000"
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        schema = response.json()
        
        # Validation basique
        required_fields = ['openapi', 'info', 'paths']
        for field in required_fields:
            if field in schema:
                print(f"   ✅ {field}: OK")
            else:
                print(f"   ❌ {field}: MANQUANT")
                return False
        
        # Vérifier les informations API
        info = schema.get('info', {})
        print(f"\n   📋 Informations API:")
        print(f"      Title:   {info.get('title')}")
        print(f"      Version: {info.get('version')}")
        print(f"      Desc:    {info.get('description', 'N/A')}")
        
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False


def print_swagger_urls():
    """
    Affiche les URLs d'accès à Swagger
    """
    print("\n" + "=" * 80)
    print("🌐 ACCÈS À SWAGGER")
    print("=" * 80)
    print()
    print("Une fois le serveur démarré, accédez à:")
    print()
    print("  📊 Swagger UI (Interactif):")
    print("     http://localhost:8000/docs")
    print()
    print("  📚 ReDoc (Documentation):")
    print("     http://localhost:8000/redoc")
    print()
    print("  🔗 Schéma OpenAPI (JSON):")
    print("     http://localhost:8000/openapi.json")
    print()
    print("=" * 80)
    print()


def main():
    """
    Fonction principale
    """
    print("\n")
    print("🚀 TEST SWAGGER UI - AlgoTrade Lab API")
    print()
    
    # Vérifier que le serveur est en cours d'exécution
    print("⏳ Vérification du serveur...")
    try:
        response = requests.get("http://localhost:8000/openapi.json", timeout=5)
        print("✅ Serveur accessible\n")
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Le serveur n'est pas accessible")
        print()
        print("Veuillez démarrer le serveur avec l'une de ces commandes:")
        print()
        print("  python run.py")
        print("  ou")
        print("  uvicorn main:app --reload")
        print()
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Exécuter les tests
    if test_swagger_endpoints():
        if validate_openapi_schema():
            print_swagger_urls()
            print("✅ Tous les tests Swagger sont PASSÉS!")
            print()
            return True
    
    print("❌ Certains tests ont ÉCHOUÉ")
    return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⛔ Test interrompu par l'utilisateur")
        sys.exit(1)
