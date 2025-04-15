import yaml
import sys

def load_config(path='config.yaml'):
    """Carga y valida la configuración"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            if not all(key in config for key in ['credentials', 'settings']):
                raise ValueError("Estructura incorrecta en config.yaml")
            return config
    except Exception as e:
        print(f"❌ Error en config.yaml: {e}")
        sys.exit(1)