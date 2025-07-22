import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

def create_sample_survey_data():
    """Crear datos de muestra para probar la aplicación"""
    
    # Generar datos de encuesta de satisfacción del cliente
    np.random.seed(42)
    n_responses = 500
    
    # Preguntas de la encuesta
    data = {
        'fecha_respuesta': [
            (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d')
            for _ in range(n_responses)
        ],
        
        'edad': np.random.normal(35, 12, n_responses).astype(int),
        
        'genero': np.random.choice(['Masculino', 'Femenino', 'Otro'], n_responses, p=[0.45, 0.5, 0.05]),
        
        'satisfaccion_general': np.random.choice([1, 2, 3, 4, 5], n_responses, p=[0.05, 0.1, 0.2, 0.4, 0.25]),
        
        'calidad_producto': np.random.choice([1, 2, 3, 4, 5], n_responses, p=[0.03, 0.07, 0.25, 0.45, 0.2]),
        
        'atencion_cliente': np.random.choice([1, 2, 3, 4, 5], n_responses, p=[0.08, 0.12, 0.3, 0.35, 0.15]),
        
        'precio_valor': np.random.choice([1, 2, 3, 4, 5], n_responses, p=[0.1, 0.15, 0.35, 0.3, 0.1]),
        
        'recomendaria': np.random.choice(['Sí', 'No', 'Tal vez'], n_responses, p=[0.6, 0.2, 0.2]),
        
        'frecuencia_compra': np.random.choice(
            ['Primera vez', 'Mensual', 'Trimestral', 'Anual'], 
            n_responses, 
            p=[0.3, 0.4, 0.2, 0.1]
        ),
        
        'canal_preferido': np.random.choice(
            ['Online', 'Tienda física', 'Teléfono', 'App móvil'], 
            n_responses, 
            p=[0.4, 0.35, 0.1, 0.15]
        ),
    }
    
    # Generar comentarios basados en satisfacción
    comentarios_positivos = [
        "Excelente servicio, muy satisfecho con la compra",
        "Producto de alta calidad, lo recomiendo totalmente",
        "Atención al cliente excepcional, resolvieron todas mis dudas",
        "Muy buena experiencia de compra, volveré a comprar",
        "Superó mis expectativas, producto increíble",
        "Servicio rápido y eficiente, muy contento",
        "Calidad precio excelente, vale la pena",
        "Personal muy amable y profesional"
    ]
    
    comentarios_neutrales = [
        "Está bien, cumple con lo esperado",
        "Producto decente, sin quejas particulares",
        "Servicio normal, nada extraordinario",
        "Está ok, podría mejorar algunos aspectos",
        "Cumple su función, precio razonable",
        "Experiencia promedio, sin problemas graves"
    ]
    
    comentarios_negativos = [
        "Muy decepcionado con el producto",
        "Servicio al cliente deficiente, no resolvieron mi problema",
        "Calidad muy por debajo de lo esperado",
        "Precio muy alto para la calidad ofrecida",
        "Tuve problemas con la entrega, muy lento",
        "No lo recomendaría, mala experiencia",
        "Producto defectuoso, no funciona correctamente",
        "Atención terrible, personal poco capacitado"
    ]
    
    comentarios = []
    for satisfaccion in data['satisfaccion_general']:
        if satisfaccion >= 4:
            comentarios.append(np.random.choice(comentarios_positivos))
        elif satisfaccion == 3:
            comentarios.append(np.random.choice(comentarios_neutrales))
        else:
            comentarios.append(np.random.choice(comentarios_negativos))
    
    data['comentarios'] = comentarios
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Ajustar edades para que estén en rango válido
    df['edad'] = df['edad'].clip(18, 80)
    
    return df

def save_sample_data():
    """Guardar datos de muestra en diferentes formatos"""
    df = create_sample_survey_data()
    
    # Guardar en CSV
    df.to_csv('data/sample_survey.csv', index=False, encoding='utf-8')
    print("✅ Datos de muestra guardados en: data/sample_survey.csv")
    
    # Guardar en Excel
    df.to_excel('data/sample_survey.xlsx', index=False)
    print("✅ Datos de muestra guardados en: data/sample_survey.xlsx")
    
    # Guardar en JSON
    df.to_json('data/sample_survey.json', orient='records', force_ascii=False, indent=2)
    print("✅ Datos de muestra guardados en: data/sample_survey.json")
    
    # Mostrar resumen
    print(f"\n📊 Resumen de datos generados:")
    print(f"   - Total de respuestas: {len(df)}")
    print(f"   - Columnas: {len(df.columns)}")
    print(f"   - Satisfacción promedio: {df['satisfaccion_general'].mean():.2f}/5")
    print(f"   - % que recomendaría: {(df['recomendaria'] == 'Sí').mean()*100:.1f}%")
    
    return df

if __name__ == "__main__":
    print("🔧 Generando datos de muestra para Survey AI Analyzer...")
    save_sample_data()
    print("\n🎉 ¡Datos de muestra creados exitosamente!")
    print("\nPuedes usar estos archivos para probar la aplicación:")
    print("   - data/sample_survey.csv")
    print("   - data/sample_survey.xlsx") 
    print("   - data/sample_survey.json")
