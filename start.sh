#!/bin/bash

echo "�� Iniciando Survey AI Analyzer..."

# Crear directorio de datos si no existe
mkdir -p data/surveys

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "❌ pip no está instalado. Por favor instálalo primero."
    exit 1
fi

# Instalar dependencias de Python
echo "📦 Instalando dependencias de Python..."
pip install -r requirements.txt

# Descargar modelos de NLTK
echo "📥 Descargando modelos de NLTK..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('vader_lexicon', quiet=True)"

# Iniciar servidor backend
echo "🔧 Iniciando servidor backend en puerto 8000..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

BACKEND_PID=$!

echo "✅ Backend iniciado con PID: $BACKEND_PID"
echo "🌐 API disponible en: http://localhost:8000"
echo "📚 Documentación en: http://localhost:8000/docs"

# Verificar si Node.js está instalado para el frontend
if command -v npm &> /dev/null; then
    echo "🎨 Iniciando frontend..."
    cd frontend
    
    # Instalar dependencias si no existen
    if [ ! -d "node_modules" ]; then
        echo "📦 Instalando dependencias de Node.js..."
        npm install
    fi
    
    # Iniciar servidor frontend
    echo "🔧 Iniciando servidor frontend en puerto 3000..."
    npm start &
    
    FRONTEND_PID=$!
    echo "✅ Frontend iniciado con PID: $FRONTEND_PID"
    echo "🌐 Aplicación web disponible en: http://localhost:3000"
    
    cd ..
else
    echo "⚠️ Node.js no está instalado. Solo se ejecutará el backend."
    echo "🌐 Para usar la interfaz web, instala Node.js y ejecuta:"
    echo "   cd frontend && npm install && npm start"
fi

echo ""
echo "🎉 Survey AI Analyzer está ejecutándose!"
echo ""
echo "Para detener la aplicación, presiona Ctrl+C"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo Survey AI Analyzer..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend detenido"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend detenido"
    fi
    
    echo "�� ¡Hasta luego!"
    exit 0
}

# Capturar señal de interrupción
trap cleanup INT

# Esperar indefinidamente
wait
