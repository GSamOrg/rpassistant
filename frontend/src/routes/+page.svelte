<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth.js';

  onMount(() => {
    if (!$authStore.user) {
      goto('/login');
    } else {
      goto('/campaigns');
    }
  });
</script>

<div class="flex items-center justify-center min-h-64">
  <div class="text-center">
    <h1 class="text-4xl font-bold text-gray-900 mb-4">
      RPG Campaign Assistant
    </h1>
    <p class="text-lg text-gray-600">
      Loading...
    </p>
  </div>
</div>