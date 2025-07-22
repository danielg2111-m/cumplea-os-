import React from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  Chip
} from '@mui/material';
import {
  Psychology as AIIcon,
  Analytics as AnalyticsIcon,
  TrendingUp as TrendingIcon,
  Insights as InsightsIcon,
  CloudUpload as UploadIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';
import { Link } from 'react-router-dom';

const HomePage = () => {
  const features = [
    {
      icon: <AIIcon sx={{ fontSize: 40, color: '#667eea' }} />,
      title: 'Análisis con IA',
      description: 'Algoritmos avanzados de machine learning para análisis profundo de sentimientos y patrones.',
      highlight: 'Inteligencia Artificial'
    },
    {
      icon: <AnalyticsIcon sx={{ fontSize: 40, color: '#764ba2' }} />,
      title: 'Estadísticas Avanzadas',
      description: 'Análisis descriptivo, correlaciones, clustering y detección automática de outliers.',
      highlight: 'Estadísticas'
    },
    {
      icon: <InsightsIcon sx={{ fontSize: 40, color: '#667eea' }} />,
      title: 'Insights Automáticos',
      description: 'Generación automática de insights y recomendaciones basadas en los datos.',
      highlight: 'Insights'
    },
    {
      icon: <TrendingIcon sx={{ fontSize: 40, color: '#764ba2' }} />,
      title: 'Visualizaciones',
      description: 'Gráficos interactivos, mapas de calor, nubes de palabras y dashboards dinámicos.',
      highlight: 'Visualización'
    },
    {
      icon: <SpeedIcon sx={{ fontSize: 40, color: '#667eea' }} />,
      title: 'Procesamiento Rápido',
      description: 'Análisis en tiempo real de grandes volúmenes de datos de encuestas.',
      highlight: 'Velocidad'
    },
    {
      icon: <UploadIcon sx={{ fontSize: 40, color: '#764ba2' }} />,
      title: 'Múltiples Formatos',
      description: 'Soporte para CSV, Excel, JSON y más formatos de datos.',
      highlight: 'Compatibilidad'
    }
  ];

  return (
    <Box sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', minHeight: '100vh' }}>
      {/* Hero Section */}
      <Container maxWidth="lg">
        <Box sx={{ pt: 8, pb: 6, textAlign: 'center', color: 'white' }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 700, mb: 3 }}>
            Máquina de Inteligencia Artificial
          </Typography>
          <Typography variant="h4" component="h2" gutterBottom sx={{ fontWeight: 400, mb: 4, opacity: 0.9 }}>
            para Análisis de Datos de Encuestas
          </Typography>
          <Typography variant="h6" sx={{ mb: 6, opacity: 0.8, maxWidth: '800px', mx: 'auto' }}>
            Transforma tus datos de encuestas en insights accionables con el poder de la inteligencia artificial. 
            Análisis de sentimientos, clustering, correlaciones y mucho más.
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 3, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              component={Link}
              to="/upload"
              variant="contained"
              size="large"
              startIcon={<UploadIcon />}
              sx={{
                background: 'rgba(255, 255, 255, 0.2)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                color: 'white',
                fontWeight: 600,
                px: 4,
                py: 1.5,
                '&:hover': {
                  background: 'rgba(255, 255, 255, 0.3)',
                }
              }}
            >
              Comenzar Análisis
            </Button>
            
            <Button
              component={Link}
              to="/dashboard"
              variant="outlined"
              size="large"
              sx={{
                border: '2px solid rgba(255, 255, 255, 0.5)',
                color: 'white',
                fontWeight: 600,
                px: 4,
                py: 1.5,
                '&:hover': {
                  border: '2px solid rgba(255, 255, 255, 0.8)',
                  background: 'rgba(255, 255, 255, 0.1)',
                }
              }}
            >
              Ver Dashboard
            </Button>
          </Box>
        </Box>
      </Container>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ pb: 8 }}>
        <Box sx={{ mb: 6, textAlign: 'center' }}>
          <Typography variant="h3" component="h2" gutterBottom sx={{ color: 'white', fontWeight: 600 }}>
            Características Principales
          </Typography>
          <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.8)', maxWidth: '600px', mx: 'auto' }}>
            Herramientas avanzadas de análisis de datos potenciadas por inteligencia artificial
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={6} lg={4} key={index}>
              <Card 
                className="feature-card"
                sx={{ 
                  height: '100%',
                  background: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: 3
                }}
              >
                <CardContent sx={{ p: 4, textAlign: 'center' }}>
                  <Box sx={{ mb: 2 }}>
                    {feature.icon}
                  </Box>
                  
                  <Chip 
                    label={feature.highlight}
                    size="small"
                    sx={{ 
                      mb: 2,
                      background: 'linear-gradient(45deg, #667eea, #764ba2)',
                      color: 'white',
                      fontWeight: 600
                    }}
                  />
                  
                  <Typography variant="h6" component="h3" gutterBottom sx={{ fontWeight: 600, color: '#333' }}>
                    {feature.title}
                  </Typography>
                  
                  <Typography variant="body1" sx={{ color: '#666', lineHeight: 1.6 }}>
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Container maxWidth="lg">
        <Box 
          sx={{ 
            textAlign: 'center', 
            py: 8,
            background: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            border: '1px solid rgba(255, 255, 255, 0.2)',
            mb: 4
          }}
        >
          <Typography variant="h4" component="h2" gutterBottom sx={{ color: 'white', fontWeight: 600 }}>
            ¿Listo para analizar tus encuestas?
          </Typography>
          <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.8)', mb: 4 }}>
            Sube tu archivo y obtén insights en minutos
          </Typography>
          
          <Button
            component={Link}
            to="/upload"
            variant="contained"
            size="large"
            startIcon={<UploadIcon />}
            sx={{
              background: 'white',
              color: '#667eea',
              fontWeight: 600,
              px: 6,
              py: 2,
              fontSize: '1.1rem',
              '&:hover': {
                background: '#f5f5f5',
                transform: 'translateY(-2px)',
                boxShadow: '0 8px 25px rgba(0, 0, 0, 0.2)',
              }
            }}
          >
            Subir Encuesta Ahora
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default HomePage;
