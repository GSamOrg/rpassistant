<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { campaignStore } from '$lib/stores/campaigns.js';
  import { authStore } from '$lib/stores/auth.js';
  
  let isLoading = true;
  let showCreateForm = false;
  let newCampaign = {
    name: '',
    rpg_system: 'Call of Cthulhu',
    description: ''
  };

  const rpgSystems = [
    'Call of Cthulhu',
    'D&D 5e',
    'Pathfinder',
    'World of Darkness',
    'Other'
  ];

  onMount(async () => {
    if (!$authStore.user) {
      goto('/login');
      return;
    }
    
    try {
      await campaignStore.loadCampaigns();
    } catch (error) {
      console.error('Failed to load campaigns:', error);
    } finally {
      isLoading = false;
    }
  });

  async function createCampaign() {
    if (!newCampaign.name || !newCampaign.rpg_system) {
      return;
    }

    try {
      await campaignStore.createCampaign(newCampaign);
      newCampaign = { name: '', rpg_system: 'Call of Cthulhu', description: '' };
      showCreateForm = false;
    } catch (error) {
      console.error('Failed to create campaign:', error);
    }
  }

  function openCampaign(campaignId) {
    goto(`/campaigns/${campaignId}`);
  }
</script>

<div class="space-y-6">
  <div class="flex justify-between items-center">
    <h1 class="text-3xl font-bold text-gray-900">My Campaigns</h1>
    <button 
      on:click={() => showCreateForm = true}
      class="btn btn-primary"
    >
      New Campaign
    </button>
  </div>

  {#if showCreateForm}
    <div class="card">
      <h2 class="text-xl font-semibold mb-4">Create New Campaign</h2>
      
      <form on:submit|preventDefault={createCampaign} class="space-y-4">
        <div>
          <label for="campaignName" class="block text-sm font-medium text-gray-700">
            Campaign Name
          </label>
          <input
            id="campaignName"
            type="text"
            bind:value={newCampaign.name}
            class="input mt-1"
            placeholder="Enter campaign name"
            required
          />
        </div>
        
        <div>
          <label for="rpgSystem" class="block text-sm font-medium text-gray-700">
            RPG System
          </label>
          <select
            id="rpgSystem"
            bind:value={newCampaign.rpg_system}
            class="input mt-1"
            required
          >
            {#each rpgSystems as system}
              <option value={system}>{system}</option>
            {/each}
          </select>
        </div>
        
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700">
            Description (Optional)
          </label>
          <textarea
            id="description"
            bind:value={newCampaign.description}
            class="input mt-1"
            rows="3"
            placeholder="Brief description of your campaign"
          ></textarea>
        </div>
        
        <div class="flex space-x-3">
          <button type="submit" class="btn btn-primary">
            Create Campaign
          </button>
          <button 
            type="button" 
            on:click={() => showCreateForm = false}
            class="btn btn-secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  {/if}

  {#if isLoading}
    <div class="text-center py-8">
      <p class="text-gray-600">Loading campaigns...</p>
    </div>
  {:else if $campaignStore.campaigns.length === 0}
    <div class="text-center py-12">
      <h3 class="text-lg font-medium text-gray-900 mb-2">No campaigns yet</h3>
      <p class="text-gray-600 mb-4">Create your first campaign to get started</p>
      <button 
        on:click={() => showCreateForm = true}
        class="btn btn-primary"
      >
        Create Your First Campaign
      </button>
    </div>
  {:else}
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {#each $campaignStore.campaigns as campaign}
        <div class="card hover:shadow-md transition-shadow cursor-pointer" on:click={() => openCampaign(campaign.id)}>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">
            {campaign.name}
          </h3>
          <p class="text-sm text-gray-600 mb-2">
            {campaign.rpg_system}
          </p>
          {#if campaign.description}
            <p class="text-gray-700 text-sm mb-4">
              {campaign.description}
            </p>
          {/if}
          <div class="text-xs text-gray-500">
            Created {new Date(campaign.created_at).toLocaleDateString()}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>