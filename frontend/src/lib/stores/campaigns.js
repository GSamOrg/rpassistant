import { writable } from 'svelte/stores';
import { authStore } from './auth.js';
import { get } from 'svelte/store';

const API_BASE = 'http://localhost:8000';

function createCampaignStore() {
  const { subscribe, set, update } = writable({
    campaigns: [],
    currentCampaign: null,
    isLoading: false
  });

  async function getAuthHeaders() {
    const auth = get(authStore);
    if (!auth.token) {
      throw new Error('Not authenticated');
    }
    return {
      'Authorization': `Bearer ${auth.token}`,
      'Content-Type': 'application/json'
    };
  }

  return {
    subscribe,
    
    async loadCampaigns() {
      update(state => ({ ...state, isLoading: true }));
      
      try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_BASE}/campaigns/`, {
          headers
        });
        
        if (!response.ok) {
          throw new Error('Failed to load campaigns');
        }
        
        const campaigns = await response.json();
        update(state => ({ ...state, campaigns, isLoading: false }));
      } catch (error) {
        update(state => ({ ...state, isLoading: false }));
        throw error;
      }
    },
    
    async createCampaign(campaignData) {
      try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_BASE}/campaigns/`, {
          method: 'POST',
          headers,
          body: JSON.stringify(campaignData)
        });
        
        if (!response.ok) {
          throw new Error('Failed to create campaign');
        }
        
        const newCampaign = await response.json();
        update(state => ({
          ...state,
          campaigns: [...state.campaigns, newCampaign]
        }));
        
        return newCampaign;
      } catch (error) {
        throw error;
      }
    },
    
    async loadCampaign(campaignId) {
      update(state => ({ ...state, isLoading: true }));
      
      try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_BASE}/campaigns/${campaignId}`, {
          headers
        });
        
        if (!response.ok) {
          throw new Error('Failed to load campaign');
        }
        
        const campaign = await response.json();
        update(state => ({ ...state, currentCampaign: campaign, isLoading: false }));
        return campaign;
      } catch (error) {
        update(state => ({ ...state, isLoading: false }));
        throw error;
      }
    },
    
    async updateCampaign(campaignId, updates) {
      try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_BASE}/campaigns/${campaignId}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(updates)
        });
        
        if (!response.ok) {
          throw new Error('Failed to update campaign');
        }
        
        const updatedCampaign = await response.json();
        update(state => ({
          ...state,
          currentCampaign: updatedCampaign,
          campaigns: state.campaigns.map(c => 
            c.id === campaignId ? updatedCampaign : c
          )
        }));
        
        return updatedCampaign;
      } catch (error) {
        throw error;
      }
    }
  };
}

export const campaignStore = createCampaignStore();