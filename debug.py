"""
Script pour debugger ton modèle directement
Lance ça pour voir exactement ce que retourne ton modèle
"""
import joblib
import pickle
import numpy as np
from pathlib import Path

def test_model():
    model_path = Path("ml/obesity_model.pkl")
    
    if not model_path.exists():
        print("❌ Modèle non trouvé!")
        return
    
    # Charge le modèle
    try:
        model = joblib.load(model_path)
        print("✅ Modèle chargé avec joblib")
    except:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("✅ Modèle chargé avec pickle")
    
    print(f"Type de modèle: {type(model)}")
    
    # Test avec tes données
    test_data = [[25, 175, 70, 0]]  # Age, Height, Weight, history
    print(f"Données test: {test_data}")
    
    # Prédiction
    prediction = model.predict(test_data)
    probabilities = model.predict_proba(test_data)
    
    print(f"\n🎯 Résultats:")
    print(f"Prédiction: {prediction}")
    print(f"Type prédiction: {type(prediction[0])}")
    print(f"Probabilités: {probabilities}")
    print(f"Shape probas: {probabilities.shape}")
    
    # Vérifie les classes du modèle
    if hasattr(model, 'classes_'):
        print(f"Classes du modèle: {model.classes_}")
        print(f"Type classes: {type(model.classes_)}")
        
        # Mapping des classes
        for i, class_name in enumerate(model.classes_):
            print(f"Index {i}: {class_name} (proba: {probabilities[0][i]:.3f})")
    
    # Test direct d'indexation
    print(f"\n🧪 Tests d'indexation:")
    try:
        print(f"probabilities[0]: {probabilities[0]}")
        print(f"probabilities[0][0]: {probabilities[0][0]}")
        print(f"probabilities[0][1]: {probabilities[0][1]}")
        
        # Test avec la prédiction comme index
        pred_value = prediction[0]
        print(f"prediction[0]: {pred_value}")
        
        # Essaie d'utiliser la prédiction comme index
        try:
            result = probabilities[0][pred_value]
            print(f"❌ Ça ne devrait pas marcher: probabilities[0][{pred_value}] = {result}")
        except Exception as e:
            print(f"✅ Erreur attendue: {e}")
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    test_model()