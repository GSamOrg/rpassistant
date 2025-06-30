<script>
  import { authStore } from '$lib/stores/auth.js';
  import { goto } from '$app/navigation';
  
  let email = '';
  let password = '';
  let isLoading = false;
  let error = '';

  async function handleLogin() {
    if (!email || !password) {
      error = 'Email and password are required';
      return;
    }

    isLoading = true;
    error = '';

    try {
      await authStore.login(email, password);
      goto('/campaigns');
    } catch (err) {
      error = err.message || 'Login failed';
    } finally {
      isLoading = false;
    }
  }

  function handleKeypress(event) {
    if (event.key === 'Enter') {
      handleLogin();
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center">
  <div class="max-w-md w-full space-y-8">
    <div class="text-center">
      <h2 class="text-3xl font-bold text-gray-900">
        Sign in to your account
      </h2>
      <p class="mt-2 text-sm text-gray-600">
        Or 
        <a href="/register" class="font-medium text-primary-600 hover:text-primary-500">
          create a new account
        </a>
      </p>
    </div>
    
    <form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
      <div class="space-y-4">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Email address
          </label>
          <input
            id="email"
            type="email"
            bind:value={email}
            on:keypress={handleKeypress}
            class="input mt-1"
            placeholder="Enter your email"
            required
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            id="password"
            type="password"
            bind:value={password}
            on:keypress={handleKeypress}
            class="input mt-1"
            placeholder="Enter your password"
            required
          />
        </div>
      </div>

      {#if error}
        <div class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
          {error}
        </div>
      {/if}

      <button
        type="submit"
        disabled={isLoading}
        class="btn btn-primary w-full"
      >
        {isLoading ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  </div>
</div>