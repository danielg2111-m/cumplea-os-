import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  Container
} from '@mui/material';
import { 
  Home as HomeIcon,
  CloudUpload as UploadIcon,
  Dashboard as DashboardIcon,
  Psychology as AIIcon
} from '@mui/icons-material';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <AppBar position="static" sx={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(10px)' }}>
      <Container maxWidth="lg">
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <AIIcon sx={{ mr: 1, color: '#667eea' }} />
            <Typography 
              variant="h6" 
              component={Link}
              to="/"
              sx={{ 
                textDecoration: 'none',
                background: 'linear-gradient(45deg, #667eea, #764ba2)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontWeight: 700
              }}
            >
              Survey AI Analyzer
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              component={Link}
              to="/"
              startIcon={<HomeIcon />}
              sx={{ 
                color: isActive('/') ? '#667eea' : '#666',
                fontWeight: isActive('/') ? 600 : 400
              }}
            >
              Inicio
            </Button>
            
            <Button
              component={Link}
              to="/upload"
              startIcon={<UploadIcon />}
              sx={{ 
                color: isActive('/upload') ? '#667eea' : '#666',
                fontWeight: isActive('/upload') ? 600 : 400
              }}
            >
              Subir Encuesta
            </Button>
            
            <Button
              component={Link}
              to="/dashboard"
              startIcon={<DashboardIcon />}
              sx={{ 
                color: isActive('/dashboard') ? '#667eea' : '#666',
                fontWeight: isActive('/dashboard') ? 600 : 400
              }}
            >
              Dashboard
            </Button>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;
