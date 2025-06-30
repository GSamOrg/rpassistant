<script>
  import '../app.css';
  import { page } from '$app/stores';
  import { authStore } from '$lib/stores/auth.js';
  
  $: isAuthPage = $page.route.id?.startsWith('/(auth)');
</script>

<div class="min-h-screen bg-gray-50">
  {#if !isAuthPage && $authStore.user}
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <a href="/" class="text-xl font-bold text-gray-900">
              RPG Assistant
            </a>
          </div>
          
          <div class="flex items-center space-x-4">
            <a href="/campaigns" class="text-gray-700 hover:text-gray-900">Campaigns</a>
            <button 
              on:click={() => authStore.logout()}
              class="btn btn-secondary"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </nav>
  {/if}
  
  <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
    <slot />
  </main>
</div>