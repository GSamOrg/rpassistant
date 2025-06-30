import { writable } from 'svelte/stores';
import { browser } from '$app/environment';

const API_BASE = 'http://localhost:8000';

function createAuthStore() {
  const { subscribe, set, update } = writable({
    user: null,
    token: null,
    isLoading: false
  });

  // Initialize from localStorage if in browser
  if (browser) {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    if (token && user) {
      set({
        user: JSON.parse(user),
        token,
        isLoading: false
      });
    }
  }

  return {
    subscribe,
    
    async login(email, password) {
      update(state => ({ ...state, isLoading: true }));
      
      try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE}/auth/token`, {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) {
          throw new Error('Invalid credentials');
        }
        
        const data = await response.json();
        const token = data.access_token;
        
        // Get user info
        const userResponse = await fetch(`${API_BASE}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (!userResponse.ok) {
          throw new Error('Failed to get user info');
        }
        
        const user = await userResponse.json();
        
        // Store in localStorage
        if (browser) {
          localStorage.setItem('token', token);
          localStorage.setItem('user', JSON.stringify(user));
        }
        
        set({ user, token, isLoading: false });
      } catch (error) {
        update(state => ({ ...state, isLoading: false }));
        throw error;
      }
    },
    
    async register(email, password, fullName) {
      update(state => ({ ...state, isLoading: true }));
      
      try {
        const response = await fetch(`${API_BASE}/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email,
            password,
            full_name: fullName
          })
        });
        
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || 'Registration failed');
        }
        
        // Auto-login after registration
        await this.login(email, password);
      } catch (error) {
        update(state => ({ ...state, isLoading: false }));
        throw error;
      }
    },
    
    logout() {
      if (browser) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
      set({ user: null, token: null, isLoading: false });
    }
  };
}

export const authStore = createAuthStore();